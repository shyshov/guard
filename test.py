#!/usr/bin/python

# -*- coding: utf-8 -*-
import RPIO
import time
import telebot
import vars
import MySQLdb

bot = telebot.TeleBot(vars.token)
telegram_id = vars.telegramId 
input_pins = (18,19,20,21,22,23,24,25,26,27)

def writeDoorState(when, state):
  db = MySQLdb.connect(vars.mysqlHost,vars.mysqUser,vars.mysqlPassword,vars.mysqlDatabase)
  cursor = db.cursor()
  sql = "INSERT INTO door(bool, date, name) VALUES (0, '%s', '%s')" % (when , state)
  try:
     # Execute the SQL command
     cursor.execute(sql)
     # Commit your changes in the database
     db.commit()
  except:
     # Rollback in case there is any error
     db.rollback()
  db.close()


for i in xrange(len(input_pins)): 
  RPIO.setup(input_pins[i], RPIO.IN, pull_up_down=RPIO.PUD_DOWN)

def write_door_state(gpio_id, val):
  if val==0:
    bot.send_message(telegram_id, "Openning")
    writeDoorState(time.strftime("%d.%m.%Y %H:%M:%S"), 'Open')
  else:
    bot.send_message(telegram_id, "Closing")
    writeDoorState(time.strftime("%d.%m.%Y %H:%M:%S"), 'Close')

RPIO.add_interrupt_callback(24, write_door_state,pull_up_down=RPIO.PUD_DOWN,threaded_callback=True, debounce_timeout_ms=50) 
RPIO.wait_for_interrupts() 