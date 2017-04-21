#!/usr/bin/env python

# Copyright (C) 2006, Red Hat, Inc.
#
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General
# Public License as published by the Free Software
# Foundation; either version 2 of the License, or (at
# your option) any later version.
#
# This program is distributed in the hope that it will
# be useful, but WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General
# Public License for more details.
#
# You should have received a copy of the GNU General
# Public License along with this program; if not,
# write to the Free Software Foundation, Inc.,
# 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301  USA

import sys
import os
import zipfile
import pygtk
import gtk
import pango
from math import *
import gtk.glade
from sugar.activity import activity
from sugar.graphics import style

class NutritionActivity(activity.Activity):
    def __init__(self, handle):
	runaslib = False
        "The entry point to the Activity"
        global page
        activity.Activity.__init__(self, handle)

        toolbox = activity.ActivityToolbox(self)
        activity_toolbar = toolbox.get_activity_toolbar()
        activity_toolbar.keep.props.visible = True
        activity_toolbar.share.props.visible = True
        self.set_toolbox(toolbox)

        toolbox.show()
        self.scrolled_window = gtk.ScrolledWindow()
        self.scrolled_window.set_policy(gtk.POLICY_NEVER,
            gtk.POLICY_AUTOMATIC)
        self.scrolled_window.props.shadow_type = \
            gtk.SHADOW_NONE

        self.protein = 0
	self.dairy = 0
	self.grains = 0
	self.fruit = 0
	self.veg = 0
	self.junk = 0

        self.xml = gtk.glade.XML("nutriGUI.glade")
	self.adviceLabel = self.xml.get_widget('advice')

	self.calcButton = self.xml.get_widget('button1')
	self.calcButton.connect('clicked', self.calculate)

	self.exitButton = self.xml.get_widget('button2')
	self.exitButton.connect('clicked', gtk.main_quit)

        self.w = self.xml.get_widget('window1')
        #self.w.connect("delete_event", gtk.main_quit)
	# Get Windows child
	self.w_child = self.w.get_child()
	self.widget = self.w_child

	self.w.fullscreen()
	
	#v1 = self.xml.get_widget('vbox1')

	# Get our Label
	#self.title = self.xml.get_widget('label1')
	self.meterImage = self.xml.get_widget('image')

	self.comboList = [self.xml.get_widget('combobox1'), self.xml.get_widget('combobox2'), self.xml.get_widget('combobox3'), self.xml.get_widget('combobox4'), self.xml.get_widget('combobox5'), self.xml.get_widget('combobox6')]

	#Listen for changes made to ComboBox options
	self.comboList[0].connect('changed', self.changed_cb) 
        self.comboList[1].connect('changed', self.changed_d)
        self.comboList[2].connect('changed', self.changed_g)
        self.comboList[3].connect('changed', self.changed_f)
        self.comboList[4].connect('changed', self.changed_v)
        self.comboList[5].connect('changed', self.changed_j)

	if not runaslib:
		self.w.show()
		gtk.main()

    def changed_cb(self, index):
	active = self.comboList[0].get_active_text()
        self.protein = active
	return active

    def changed_d(self, index):
	active = self.comboList[1].get_active_text()
        self.dairy = active
	return active

    def changed_g(self, index):
	active = self.comboList[2].get_active_text()
        self.grains = active
	return active

    def changed_f(self, index):
	active = self.comboList[3].get_active_text()
        self.fruit = active
	return active

    def changed_v(self, index):
	active = self.comboList[4].get_active_text()
        self.veg = active
	return active

    def changed_j(self, index):
	active = self.comboList[5].get_active_text()
        self.junk = active
	return active

    def get_active_text(combobox):
	model = combobox.get_model()
	active = combobox.get_active()  
	if active < 0:
	    return None
	return model[active][0]


    def calculate(self, something):
	catPoints = 20
	advice = ""
	proPts = 0
	proPts = catPoints - (abs(2 - int(self.protein)) * 10)
	dairyPts = catPoints - (abs(3 - int(self.dairy)) * 6.67)
	grainsPts = catPoints - (abs(6 - int(self.grains)) * 3.33)
	fruitPts = catPoints - (abs(2 - int(self.fruit)) * 10)
	vegPts = catPoints - (abs(3 - int(self.dairy)) * 6.67)
	junkPts = -3 * int(self.junk)
	totalPts = proPts + dairyPts + grainsPts + fruitPts + vegPts + junkPts
	if (totalPts <=20):
	    self.meterImage.set_from_file('meter.png')
	elif (totalPts <= 40):
	    self.meterImage.set_from_file('orange.png')
	elif (totalPts <= 60):
	    self.meterImage.set_from_file('yellow.png')
	elif (totalPts <= 80):
	    self.meterImage.set_from_file('green.png')
	else:
	    self.meterImage.set_from_file('blue.png')
	if (totalPts != 100):
	    advice = "You should eat...\n"
	if (self.protein != 2):
	    advice = advice + "2 servings of protein\n"
	if (self.dairy != 3):
	    advice = advice + "3 servings of dairy\n"
	if (self.grains != 6):
	    advice = advice + "6 servings of grains\n"
	if (self.fruit != 2):
	    advice = advice + "2 servings of fruit\n"
	if (self.veg != 3):
	    advice = advice + "3 servings of vegetables\n"
	if (self.junk > 2):
	    advice = advice + "limit your junk food"
	
	self.adviceLabel.set_text(advice)

    

def make_new_filename(self, filename):
    partition_tuple = filename.rpartition('/')
    return partition_tuple[2]
				
#if __name__ == '__main__':
#    nutrition(False)
    
