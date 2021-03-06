#!/usr/bin/env python

import config

from collections import defaultdict
import re

import gdata.spreadsheet.service
import requests

doctrines = {
	'Harpy': {
		'Pseudoelectron Containment Field I': 1,
		'Magnetic Field Stabilizer II': 2,

		'Adaptive Invulnerability Field II': 1,
		'Upgraded EM Ward Amplifier I': 1,
		'1MN Afterburner II': 1,
		'F-90 Positional Sensor Subroutines': 1,

		'150mm Railgun II': 4,

		'Small Processor Overclocking Unit I': 1,
		'Small Core Defense Field Extender I': 1,
	},

	'Burst': {
		'Damage Control II': 1,
		'Beta Reactor Control: Capacitor Power Relay I': 2,

		'Medium Shield Extender II': 1,
		'EM Ward Amplifier II': 1,
		'1MN Afterburner II': 1,

		'Small Remote Shield Booster II': 3,

		'Small Capacitor Control Circuit I': 2,
		'Small Core Defense Field Extender I': 1,
	},

	'Crow': {
		'Ballistic Control System II': 1,
		'Nanofiber Internal Structure II': 1,
		'Micro Auxiliary Power Core I': 1,

		'Medium Azeotropic Ward Salubrity I': 1,
		'Warp Disruptor II': 1,
		'F-90 Positional Sensor Subroutines': 1,
		'Limited 1MN Microwarpdrive I': 1,

		"Upgraded 'Malkuth' Light Missile Launcher": 3,

		'Small Ancillary Current Router I': 1,
		'Small Hydraulic Bay Thrusters I': 1,
	},

	'Augoror Navy Issue': {
		'Damage Control II': 1,
		'Armor Thermic Hardener II': 1,
		'Armor Kinetic Hardener II': 1,
		'Armor Explosive Hardener II': 1,
		'1600mm Reinforced Steel Plates II': 1,
		'Heat Sink II': 2,

		'10MN Afterburner II': 1,
		'Small Capacitor Booster II': 1,
		'Faint Epsilon Warp Scrambler I': 1,

		'Focused Medium Pulse Laser II': 3,
		'Medium Unstable Power Fluctuator I': 2,

		'Medium Anti-EM Pump I': 1,
		'Medium Trimark Armor Pump I': 2,
	},

	'Augoror': {
		'Damage Control II': 1,
		'Armor Thermic Hardener II': 1,
		'Armor Kinetic Hardener II': 1,
		'Armor Explosive Hardener II': 1,
		'800mm Reinforced Steel Plates II': 1,

		'10MN Afterburner II': 1,
		'Conjunctive Radar ECCM Scanning Array I': 2,

		"Medium 'Solace' Remote Armor Repairer": 3,
		"Medium 'Regard' Remote Capacitor Transmitter": 2,

		'Medium Anti-EM Pump I': 1,
		'Medium Trimark Armor Pump I': 2,
	},

	'Omen Navy Issue': {
		'Damage Control II': 1,
		'Armor Thermic Hardener II': 1,
		'Armor Kinetic Hardener II': 1,
		'Armor Explosive Hardener II': 1,
		'1600mm Reinforced Rolled Tungsten Plates I': 1,
		'Heat Sink II': 2,

		'10MN Afterburner II': 1,
		'Tracking Computer II': 1,
		'Small Capacitor Booster II': 1,

		'Heavy Pulse Laser II': 4,

		'Medium Ancillary Current Router I': 1,
		'Medium Anti-EM Pump I': 1,
		'Medium Trimark Armor Pump I': 1,
	},

	'Maller': {
		'Focused Medium Pulse Laser II': 5,

		'10MN Afterburner II': 1,
		'J5b Phased Prototype Warp Scrambler I': 1,
		'Small Capacitor Booster II': 1,

		'Damage Control II': 1,
		'Energized Adaptive Nano Membrane II': 2,
		'1600mm Reinforced Steel Plates II': 1,
		'Heat Sink II': 2,

		'Medium Trimark Armor Pump I': 3,
	},

	'Armageddon': {
		"'Arbalest' Cruise Launcher I": 5,
		'Drone Link Augmentor I': 1,
		'Heavy Unstable Power Fluctuator I': 1,

		'Prototype 100MN Microwarpdrive I': 1,
		'Omnidirectional Tracking Link I': 2,
		'Heavy Electrochemical Capacitor Booster I': 1,

		'Damage Control II': 1,
		'Energized Adaptive Nano Membrane II': 2,
		'Reactive Armor Hardener': 1,
		'1600mm Reinforced Steel Plates II': 2,
		'Drone Damage Amplifier II': 1,

		'Large Trimark Armor Pump I': 3,
	},

	'Guardian': {
		"Large 'Solace' Remote Armor Repairer": 3,
		"Medium 'Solace' Remote Armor Repairer": 1,
		"Large 'Regard' Remote Capacitor Transmitter": 2,

		'10MN Afterburner II': 1,
		'Conjunctive Radar ECCM Scanning Array I': 1,

		'Damage Control II': 1,
		'True Sansha Armor EM Hardener': 1,
		'Energized Adaptive Nano Membrane II': 1,
		'Armor Thermic Hardener II': 1,
		'1600mm Reinforced Rolled Tungsten Plates I': 1,

		'Medium Ancillary Current Router I': 2,
	},

	'Zealot': {
		'Damage Control II': 1,
		'Armor EM Hardener II': 1,
		'Armor Thermic Hardener II': 1,
		'Adaptive Nano Plating II': 1,
		'1600mm Reinforced Steel Plates II': 1,
		'Heat Sink II': 2,

		'10MN Afterburner II': 1,
		'Tracking Computer II': 2,

		'Heavy Pulse Laser II': 5,

		'Medium Ancillary Current Router I': 1,
		'Medium Trimark Armor Pump I': 1,
	},

	'Loki': {
		'Internal Force Field Array I': 1,
		'Imperial Navy Energized Adaptive Nano Membrane': 1,
		'True Sansha Armor Kinetic Hardener': 1,
		'True Sansha Armor Explosive Hardener': 1,
		'1600mm Reinforced Steel Plates II': 1,
		'Gyrostabilizer II': 1,

		'10MN Afterburner II': 1,
		'Warp Disruptor II': 1,
		'Fleeting Propulsion Inhibitor I': 2,

		'720mm Howitzer Artillery II': 6,

		'Medium Ancillary Current Router I': 1,
		'Medium Trimark Armor Pump I': 2,

		'Loki Defensive - Adaptive Augmenter': 1,
		'Loki Electronics - Immobility Drivers': 1,
		'Loki Engineering - Power Core Multiplier': 1,
		'Loki Offensive - Turret Concurrence Registry': 1,
		'Loki Propulsion - Fuel Catalyst': 1,
	},

	'Proteus': {
		'Damage Control II': 1,
		'Armor EM Hardener II': 1,
		'Energized Adaptive Nano Membrane II': 1,
		'Armor Explosive Hardener II': 1,
		'1600mm Reinforced Steel Plates II': 1,
		'Magnetic Field Stabilizer II': 2,

		'10MN Afterburner II': 1,
		'Small Capacitor Booster II': 1,
		'Tracking Computer II': 1,

		'250mm Railgun II': 6,

		'Medium Trimark Armor Pump I': 3,

		'Proteus Defensive - Augmented Plating': 1,
		'Proteus Electronics - Dissolution Sequencer': 1,
		'Proteus Engineering - Power Core Multiplier': 1,
		'Proteus Offensive - Dissonic Encoding Platform': 1,
		'Proteus Propulsion - Localized Injectors': 1,
	},

	'Sabre': {
		'125mm Gatling AutoCannon II': 6,
		'Prototype Cloaking Device I': 1,
		'Interdiction Sphere Launcher I': 1,

		'Medium Shield Extender II': 1,
		'Adaptive Invulnerability Field II': 1,
		'Medium Shield Extender II': 1,
		'Limited 1MN Microwarpdrive I': 1,

		'Nanofiber Internal Structure II': 2,

		'Small Core Defense Field Extender I': 2,
	},


	'Heretic': {
		"'Malkuth' Rocket Launcher I": 6,
		'Interdiction Sphere Launcher I': 1,
		'Prototype Cloaking Device I': 1,

		'Medium Shield Extender II': 2,
		'Limited 1MN Microwarpdrive I': 1,

		'Nanofiber Internal Structure II': 2,
		'Micro Auxiliary Power Core I': 1,

		'Small Anti-EM Screen Reinforcer II': 1,
		'Small Core Defense Field Extender I': 1,
	},

	'Flycatcher': {
		"'Malkuth' Rocket Launcher I": 6,
		'Prototype Cloaking Device I': 1,
		'Interdiction Sphere Launcher I': 1,

		'Medium Shield Extender II': 1,
		'Adaptive Invulnerability Field II': 1,
		'Medium Shield Extender II': 1,
		'Limited 1MN Microwarpdrive I': 1,
		'Upgraded EM Ward Amplifier I': 1,

		'Micro Auxiliary Power Core I': 1,

		'Small Processor Overclocking Unit I': 1,
		'Small Core Defense Field Extender I': 1,
	},
}

def ssp():
	spreadsheet_id = 'tKun0LlHgUgJfYLh7Zu5sjA'
	worksheet_id = 'od6'

	gd_client = gdata.spreadsheet.service.SpreadsheetsService()
	gd_client.email = config.ssp.email
	gd_client.password = config.ssp.password
	gd_client.ProgrammaticLogin()

	list_feed = gd_client.GetListFeed(spreadsheet_id, worksheet_id)
	for i, entry in enumerate(list_feed.entry):
		if entry.custom['paidoutby'].text:
			continue
		# un-atom the feed
		row = {}
		for k, v in entry.custom.items():
			if k == '_d415a':
				k = 'timestamp'
			row[k] = v.text

		try:
			yield process_row(row)
		except:
			yield 'error processing %s' % row['linkyourkillmailyouwantreimbursed']

def process_row(row):
	killurl = row['linkyourkillmailyouwantreimbursed']
	if killurl.startswith('http://j4lp.eve-kill.net/'):
		resp = requests.get(killurl)
		match = re.search('zkillboard.com/detail/(\d+)', resp.text)
		kill_id = match.group(1)
	else:
		split = killurl.split('/')
		kill_id = split[-1] or split[-2]
	kill = whelp(kill_id)
	ship_name, total_diff, diff = generate_report(kill)
	return {
		'timestamp': row['timestamp'],
		'character_name': kill['victim']['character_name'],
		'kill_id': kill_id,
		'fc': row['namethefcforyourop'],
		'ship_name': ship_name,
		'total_diff': total_diff,
		'diff': diff,
	}

rs = requests.Session()
def whelp(kill_id):
	resp = rs.get('http://api.whelp.gg/kill/' + kill_id)
	return resp.json()

def generate_report(kill):
	ship_name = kill['victim']['ship_name']
	diff = []
	doctrine = doctrines.get(ship_name)
	if doctrine is not None:
		fit = defaultdict(int)
		for slot in ['high', 'medium', 'low', 'rig']:
			for item in kill['items'].get(slot, {}):
				if not item.get('charge'):
					fit[item['item_name']] += 1

		for item_name, count in doctrine.items():
			fit[item_name] -= count

		total_diff = 0
		for item_name, count in fit.items():
			if count != 0:
				total_diff += abs(count)
				if count > 0:
					count = '+%d' % count
				diff.append((count, item_name))
	else:
		total_diff = None
	return ship_name, total_diff, diff

if __name__ == '__main__':
	for r in ssp():
		if isinstance(r, dict):
			print '%s\t%s\tFC:%s\n    %s\thttp://www.whelp.gg/kill/%s' % (
				r['timestamp'], r['character_name'], r['fc'],
				r['ship_name'], r['kill_id']
			)
			for d in r['diff']:
				print '        %s %s' % d
			if r['total_diff'] is not None:
				print '    total diff: %d' % r['total_diff']
			else:
				print '    (not doctrine)'
		else:
			print r
		print
