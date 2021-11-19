#!/usr/bin/env python3
#
# IP: HILICS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket
import struct


### This class provides the ability to send/receive sensor/actuator 
### values to/from the PLC over Ethernet/IP. This requires a network 
### connection between the RPi and the MicroLogix 1100.
###
class MicroLogixComm:

	__init__(self, ip='192.168.107.3'):
		self.ip = ip
		self.port = 44818


	### Connect to the PLC and register a session
	###
	### Returns True if connection is successful
	###
	def connect(self):
		try:
			self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			self.sock.connect((self.ip, 44818))	
			self._register_session()
			self.slot = 0
			self.context = 0
		except:
			print('Error: MicroLogixComm.connect() Failed to connect to PLC')
			
			return False

		return True


	
	### Queries for status of PLC
	### If everything is working you should see something like:
	### b'o\x008\x00\xf40\xeb\x0e\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x04\x02\x00\x00\x00\x00\x00\xb2\x00(\x00\xcb\x00\x00\x00\x07M\x00\x11-)\x04F\x00\xee\x03\x00\xeeJ\x9c#1763-LEC   \x00\x00&\x00Sp0\xfc\x01'
	###
	### Note the '1763-LEC'
	###
	def test_connection(self):
		
		pccc_object = bytes.fromhex('4b0220672401074d00112d29040600ee0303')
		
		response = self._send_pccc_object(pccc_object)

		if b'1763-LEC' in response:
			print('Connection good')
			return True
		else:
			print('Error: Invalid response received')
			return False

			

	### Removes all forces on the output file 
	### Not sure what all it affects, but it at least resets the relays
	###
	def remove_forces(self):
		print('Removing all forces')
		
		pccc_object = b'\x4b\x02\x20\x67\x24\x01\x07\x4d\x00\x11\x2d\x29\x04\x0f\x00\xc9\x5f\x63\x0f'
		
		# This one is Copy -> ...as a Hex String
		pccc_object = bytes.fromhex('4b0220672401074d00112d29040f00c95f630f')
		
		response = self._send_pccc_object(pccc_object)




	### Write a 2-byte integer value to the given file number and element
	###
	def write_integer(self, file_num, element, value):
		
		file_type = 0x89

		pccc_object = bytes.fromhex('4b0220672401074d007a1aac350f00651faa02') 
		
		pccc_object += struct.pack('B', file_num)
		pccc_object += struct.pack('B', file_type)
		pccc_object += struct.pack('<H', element)
		pccc_object += struct.pack('<H', value)

		response = self._send_pccc_object(pccc_object)

		
		# 0 - 4
		# 0x0e - File number
		# 0x89 - File type Integer
		# 2 bytes - Element number
		# 2 bytes - value
		# 4b0220672401074d007a1aac350f00ff90aa02 0e 89 0000 0f00
		# 4b0220672401074d007a1aac350f00bb93aa02 0e 89 0100 2100
		# 4b0220672401074d007a1aac350f003a94aa02 0e 89 0200 3700
		# 4b0220672401074d007a1aac350f00ae94aa02 0e 89 0300 4200
		# 4b0220672401074d007a1aac350f001c95aa02 0e 89 0400 4d00



		
	### Send the given packet (no modifications are made prior to sending
	###
	def _send(self, packet):
		self.sock.send(packet)
	
	### Get the response from the PLC
	###
	def _recv(self):
		return self.sock.recv(65536)



	### Registers an ENIP session with the PLC
	###
	def _register_session(self):

		reg = bytes.fromhex('65000400000000000000000000000000000000000000000001000000')
		
		self._send(reg)
	
		response = self._recv()
		self.session = response[4:8]
	
		# The session ID is stored in self.session
		# in a format ready for _wrapENIPHeader
		return self.session
		

	### Prepends the ENIP "Encapsulation Header" to the packet
	###
	def _wrapENIPHeader(self, data, command=b'\x70\x00'):
	
		context = struct.pack('<Q', self.context)
		leng = struct.pack('<H', len(data))
		status = b'\x00\x00\x00\x00'
		options = b'\x00\x00\x00\x00'
	
		header = command + leng + self.session + status + context + options
		return header + data


	### Prepends the ENIP "Command Specific Data" header
	###
	def _wrapCIPHeader(self, data):
		hdr = bytes.fromhex('000000000a00020000000000b200')
		
		leng = struct.pack('<H', len(data))
		
		pkt = hdr + leng + data
		
		return pkt
		

	### This expects the bytes from "PCCC Command Data" field in Wireshark
	###
	def _send_pccc_object(self, data):
		
		p = self._wrapCIPHeader(data)
		
		p = self._wrapENIPHeader(p, b'\x6F\x00')
		self._send(p)
		return self._recv()








