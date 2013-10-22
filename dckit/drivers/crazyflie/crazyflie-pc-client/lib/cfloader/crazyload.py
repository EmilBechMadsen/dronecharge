#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#     ||          ____  _ __
#  +------+      / __ )(_) /_______________ _____  ___
#  | 0xBC |     / __  / / __/ ___/ ___/ __ `/_  / / _ \
#  +------+    / /_/ / / /_/ /__/ /  / /_/ / / /_/  __/
#   ||  ||    /_____/_/\__/\___/_/   \__,_/ /___/\___/
#
#  Copyright (C) 2011-2013 Bitcraze AB
#
#  Crazyflie Nano Quadcopter Client
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.

#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA  02110-1301, USA.

#Crazy Loader bootloader utility
#Can reset bootload and reset back the bootloader

import sys

import cflib.crtp
from cflib.bootloader.cloader import Cloader

#Initialise the CRTP link driver
link = None
cload = None
try:
    cflib.crtp.init_drivers()
    link = cflib.crtp.get_link_driver("radio://0")
except(Exception):
    print "=============================="
    print " CrazyLoader Flash Utility"
    print "=============================="
    print
    print " Usage:", sys.argv[0], "[CRTP options] <action> [parameters]"
    print
    print "The CRTP options are described above"
    print
    print "Crazyload option:"
    print "   info        : Print the info of the bootloader and quit."
    print "                 Will let the target in bootloader mode"
    print "   reset       : Reset the device in firmware mode"
    print "   flash <img> : flash the <img> binary file from the first"
    print "                 possible  page in flash and reset to firmware"
    print "                 mode."
    sys.exit(0)
except Exception as e:
    print "CRTP Driver loading error:", e
    if link:
        link.close()
    sys.exit(-1)

#Set the default parameters
#Default to the arnaud's copter
cpu_id = "32:00:6e:06:58:37:35:32:60:58:01:43"
clink = "radio://0/110"
action = "info"
boot = "cold"

#Analyse the command line parameters
sys.argv = sys.argv[1:]
argv = []

i = 0
while i < len(sys.argv):
    if sys.argv[i] == "-i":
        i += 1
        cpu_id = sys.argv[i]
    elif sys.argv[i] == "--cold-boot" or sys.argv[i] == "-c":
        boot = "cold"
    else:
        argv += [sys.argv[i]]
    i += 1
sys.argv = argv

#Analyse the command
if len(sys.argv) < 1:
    action = "info"
elif sys.argv[0] == "info":
    actrion = "info"
elif sys.argv[0] == "reset":
    action = "reset"
elif sys.argv[0] == "flash":
    #print len(sys.argv)
    if len(sys.argv) < 2:
        print "The flash action require a file name."
        link.close()
        sys.exit(-1)
    action = "flash"
    filename = sys.argv[1]
else:
    print "Action", sys.argv[0], "unknown!"
    link.close()
    sys.exit(-1)

try:
    #Initialise the cflib
    cload = Cloader(link, clink)

    #########################################
    # Get the connection with the bootloader
    #########################################
    #The connection is done by reseting to the bootloader (default)
    if boot == "reset":
        sys.stdout.write("Reset to bootloader mode ...")
        sys.stdout.flush()
        if cload.reset_to_bootloader(cload.decode_cpu_id(cpu_id)):
            print " Done."
        else:
            print "\nFailed!\nThe loader with the ID",
            print cpu_id, "does not answer."
            cload.close()
            sys.exit(-1)
    else:  # The connection is done by a cold boot ...
        print "Restart the CrazyFlie you want to bootload in the next",
        print " 10 seconds ..."

        if cload.coldboot():
            print "Connection established!"
        else:
            print "Cannot connect the bootloader!"
            cload.close()
            sys.exit(-1)

    ######################################
    # Doing something (hopefully) usefull
    ######################################
    print "Flash pages: %d | Page size: %d | Buffer pages: %d |"\
          " Start page: %d" % (cload.flash_pages, cload.page_size,
                               cload.buffer_pages, cload.start_page)
    print "%d KBytes of flash avaliable for firmware image." % (
          (cload.flash_pages - cload.start_page) * cload.page_size / 1024)

    if action == "info":
        None  # Already done ...
    elif action == "reset":
        print
        print "Reset in firmware mode ..."
        cload.reset_to_firmware(cload.decode_cpu_id(cpu_id))
        print "Done!"
    elif action == "flash":
        print
        f = open(filename, "rb")
        if not f:
            print "Canno open image file", filename
            raise Exception()
        image = f.read()
        f.close()

        if len(image) > ((cload.flash_pages - cload.start_page) *
                         cload.page_size):
            print "Error: Not enough space to flash the image file."
            raise Exception()

        sys.stdout.write(("Flashing %d bytes (%d pages) " % ((len(image) - 1),
                         int(len(image) / cload.page_size) + 1)))
        sys.stdout.flush()

        #For each page
        ctr = 0  # Buffer counter
        for i in range(0, int((len(image) - 1) / cload.page_size) + 1):
            #Load the buffer
            if ((i + 1) * cload.page_size) > len(image):
                cload.upload_buffer(ctr, 0, image[i * cload.page_size:])
            else:
                cload.upload_buffer(ctr, 0, image[i * cload.page_size:
                                                  (i + 1) * cload.page_size])

            ctr += 1

            sys.stdout.write(".")
            sys.stdout.flush()

            #Flash when the complete buffers are full
            if ctr >= cload.buffer_pages:
                sys.stdout.write("%d" % ctr)
                sys.stdout.flush()
                if not cload.write_flash(0,
                                         cload.start_page + i - (ctr - 1),
                                         ctr):
                    print "\nError during flash operation (code %d). Maybe"\
                          " wrong radio link?" % cload.error_code
                    raise Exception()

                ctr = 0

        if ctr > 0:
            sys.stdout.write("%d" % ctr)
            sys.stdout.flush()
            if not cload.write_flash(
                                 0,
                                 (cload.start_page +
                                  (int((len(image) - 1) / cload.page_size)) -
                                  (ctr - 1)),
                                 ctr):
                print "\nError during flash operation (code %d). Maybe wrong"\
                      "radio link?" % cload.error_code
                raise Exception()
        print

        print "Reset in firmware mode ..."
        cload.reset_to_firmware(cload.decode_cpu_id(cpu_id))
        print "Done!"
    else:
        None
finally:
    #########################
    # Closing the connection
    #########################
    if (cload is not None):
        cload.close()
