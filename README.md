# BWC Simulation  
This pack works with Brocade Workflow Composer (BWC) to simulate the possibilities of Zero Touch Provisioning (ZTP).

BWC is a platform for integration and automation across services and tools. It ties together your existing infrastructure and application environment so you can more easily automate that environment. It has a particular focus on taking actions in response to events.

Speed up deployment with automation using Brocade’s Workflow Composer (BWC) or StackStorm.

## Overview
As a Ruckus AP is plugged into a Brocade ICX, it triggers a Dot1x and MAC-AUTH sequence that will fail.  Upon authentication failure, the ICX forwards a syslog message to BWC containing the AP's mac address and the Ethernet port.  BWC monitors the syslog file to determine whether the message is an authentication failure and the mac matches a valid Ruckus AP. If so, a BWC trigger will be set, and a rule matched initiating a workflow to reconfigure the ICX switch.

This pack is for simulation purposes only and uses webhooks and a web GUI to simulate plugging an AP into a Switch.


## Getting Started
The following information is a quick start guide on how to get this pack up and running along with BWC.

## Prereqs:
1. Brocade Workflow Composer (BWC)
2. MySQL Server

## Prerequisites Installation
### Install BWC
		curl -sSL -O https://brocade.com/bwc/install/install.sh && chmod +x install.sh
		./install.sh --user=st2admin --password=Ch@ngeMe --license=<License-Key>
(The username: “st2admin” and password: “Ch@ngeMe” is the default and can be changed)

### Install MySQL Server:
		sudo apt-get install mysql-server
		sudo mysql_secure_installation
(The username and password will be needed later on.)

### Create the database and tables in MySQL
		mysql -u <username> -p
		CREATE database users;
		USE users;
		CREATE table failures (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, timestamp VARCHAR(20), switch_name VARCHAR(30), mac VARCHAR(20), ip VARCHAR(20), device VARCHAR(30), port VARCHAR (10));
		CREATE table authorized (id INT NOT NULL PRIMARY KEY AUTO_INCREMENT, timestamp VARCHAR(20), switch_name VARCHAR(30), mac VARCHAR(20), base_mac VARCHAR(20), ip VARCHAR(20), device VARCHAR(30), port varchar (10));

Add your authorized macs and device names to the authorized table. Writing a script to do this would be the most efficient way to do this. But the command below demonstrates how this can be done in MySQL:
		
		INSERT INTO authorized (mac, device) values('0000.0000.0000', 'Ruckus_AP_BLD1');

This pack contains an action, update_db_spreadsheet, that takes in an excel file, sheetname, and column names to populate the database with the table schema described above.

## Setup BWC Datastore
Ensure that you've set up BWC for encrypted datastore. See https://docs.stackstorm.com/datastore.html

And then add the following items (replacing it with your username and password)

		st2 key set campus_ztp.username 'ICX_Switch_SSH_Username'
		st2 key set campus_ztp.password 'ICX_Switch_SSH_Passworsd' --encrypt
		st2 key set campus_ztp.enable_username 'ICX_Switch_Enable_Username'
		st2 key set campus_ztp.enable_password 'ICX_Switch_Enable_Password' –encrypt
		st2 key set campus_ztp.db_user 'MySQL_Username' --encrypt
		st2 key set campus_ztp.db_pass 'MySQL_Password' --encrypt
		st2 key set campus_ztp.db_name 'users’ --encrypt
		st2 key set campus_ztp.db_addr '127.0.0.1' --encrypt
		st2 key set campus_ztp.ruckus_controller_username 'Ruckus_Controller_Username'
		st2 key set campus_ztp.ruckus_controller_password 'Ruckus_Controller_Password' --encrypt
		st2 key set campus_ztp.ruckus_controller_enable_username 'Ruckus_Controller_Enable_Username'
		st2 key set campus_ztp.ruckus_controller_enable_password 'Ruckus_Controller_Enable_Password' --encrypt


## Pack Installation
### Via git

		st2 pack install https://github.com/pjimmybrcd/bwc_simulation.git
		st2ctl reload

### Manual Install
You can also move the entire pack to the /opt/stackstorm/packs/ directory then install by issuing the following commands.

1. Rename the folder to campus_ztp
2. Move the campus_ztp folder to /opt/stackstorm/packs/
3. Load the pack

		st2ctl reload
		st2 run packs.setup_virtualenv packs=ztp

To view the pack online navigate to https://github.com/pjimmybrcd/bwc_simulation

## Pack Removal
To remove an installed pack from BWC do the following:

		st2 pack remove ztp

## Open BWC GUI
Open the internet browser and navigate to: http://bwc_ip_address

## License
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
