# coding: utf-8
import binascii
import sys
import numpy as np
sys.setrecursionlimit(1000000)

class vec2binary():
    def __init__(self, header, truck, midi_numpy, time):
        self.header = header
        self.truck = truck
        # TODO: トラックチャネルのデータ部分のデータ長は後々midiを作成してから変更可能にする。
        self.midi_numpy = midi_numpy
        self.midi_ary = []
        self.T = time
        self.detailed_ary = [[0 for _ in range(128)] for _ in range(self.T)]

    def set_header(self):
        chunck_type = [byt for byt in self.header['chunk_type']]
        header_size = [byt for byt in self.header['header_size']]
        format = [byt for byt in self.header['format']]
        track = [byt for byt in self.header['track']]
        time_unit = [byt for byt in self.header['time_unit']]
        header_data = [chunck_type, header_size, format, track, time_unit]
        for header_ary in header_data:
            for byt in header_ary:
                self.midi_ary.append(byt)

    def set_truck(self):
        truck_type = [byt for byt in self.truck['truck_chunk']]
        data_length = ['00', '00', '00', '00']
        truck_data = [truck_type, data_length]
        for truck_ary in truck_data:
            for byt in truck_ary:
                self.midi_ary.append(byt)

    def numpy2ary(self):
        time_unit = eval('0x' + self.header['time_unit'][0] + self.header['time_unit'][1])
        sixteenth = int(time_unit / 4)
        # print(self.detailed_ary[29951])

        for vec_index, vec in enumerate(self.midi_numpy):
            for index, elem in enumerate(vec):
                if elem > 0:
                    start = vec_index*sixteenth
                    end = start + sixteenth
                    for i in range(start, end):
                        if i < self.T:
                            self.detailed_ary[i][index] = int(elem)
                        else:
                            break