#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Not titled yet
# GNU Radio version: 3.10.1.1

from packaging.version import Version as StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import filter
from gnuradio.filter import firdes
from gnuradio import gr
from gnuradio.fft import window
import sys
import signal
from PyQt5 import Qt
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
from gnuradio import gr, pdu
from gnuradio import network
from gnuradio import pdu
from gnuradio import qtgui
from gnuradio import uhd
import time
import satellites



from gnuradio import qtgui

class AX25_Tx(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Not titled yet", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Not titled yet")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "AX25_Tx")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.multiplier = multiplier = 10
        self.data_rate = data_rate = 9600
        self.samp_rate = samp_rate = data_rate*multiplier
        self.rf_multiplier = rf_multiplier = 1
        self.freq = freq = 145830000

        ##################################################
        # Blocks
        ##################################################
        if "int" == "int":
        	isFloat = False
        	scaleFactor = 1
        else:
        	isFloat = True
        	scaleFactor = 1

        _freq_dial_control = qtgui.GrDialControl('Frequency', self, 145780000,145880000,145830000,"default",self.set_freq,isFloat, scaleFactor, 100, True, "'value'")
        self.freq = _freq_dial_control

        self.top_layout.addWidget(_freq_dial_control)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
            ",".join(("", '')),
            uhd.stream_args(
                cpu_format="fc32",
                args='',
                channels=list(range(0,1)),
            ),
            "",
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate*rf_multiplier)
        self.uhd_usrp_sink_0.set_time_unknown_pps(uhd.time_spec(0))

        self.uhd_usrp_sink_0.set_center_freq(freq, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.uhd_usrp_sink_0.set_normalized_gain(1, 0)
        self.satellites_nrzi_encode_0 = satellites.nrzi_encode()
        self.satellites_kiss_to_pdu_0 = satellites.kiss_to_pdu(True)
        self.satellites_hdlc_framer_0 = satellites.hdlc_framer(preamble_bytes=48, postamble_bytes=8)
        self.pdu_pdu_to_tagged_stream_0 = pdu.pdu_to_tagged_stream(gr.types.byte_t, 'packet_len')
        self.pdu_pdu_to_stream_x_0 = pdu.pdu_to_stream_b(pdu.EARLY_BURST_APPEND, 64)
        self.network_udp_sink_0 = network.udp_sink(gr.sizeof_short, 1, 'localhost', 7355, 0, 1472, True)
        self.network_socket_pdu_0 = network.socket_pdu('UDP_SERVER', '0.0.0.0', '1234', 10000, False)
        self.interp_fir_filter_xxx_1 = filter.interp_fir_filter_ccc(rf_multiplier, [1,0,0,0])
        self.interp_fir_filter_xxx_1.declare_sample_delay(0)
        self.interp_fir_filter_xxx_0 = filter.interp_fir_filter_fff(1, [0.06480373442173004,0.14118190109729767,0.24622690677642822,0.3437711000442505,0.38422060012817383,0.3437711000442505,0.24622690677642822,0.14118190109729767,0.06480373442173004,0.02381213940680027])
        self.interp_fir_filter_xxx_0.declare_sample_delay(0)
        self.digital_scrambler_bb_0 = digital.scrambler_bb(0x21, 0x00, 16)
        self.blocks_repeat_0 = blocks.repeat(gr.sizeof_char*1, multiplier)
        self.blocks_float_to_short_0 = blocks.float_to_short(1, 5000)
        self.blocks_char_to_float_0 = blocks.char_to_float(1, 1)
        self.blocks_add_const_vxx_0 = blocks.add_const_ff(-0.5)
        self.analog_nbfm_tx_0 = analog.nbfm_tx(
        	audio_rate=samp_rate,
        	quad_rate=samp_rate,
        	tau=75e-6,
        	max_dev=3e3,
        	fh=-1.0,
                )


        ##################################################
        # Connections
        ##################################################
        self.msg_connect((self.network_socket_pdu_0, 'pdus'), (self.pdu_pdu_to_stream_x_0, 'pdus'))
        self.msg_connect((self.satellites_hdlc_framer_0, 'out'), (self.pdu_pdu_to_tagged_stream_0, 'pdus'))
        self.msg_connect((self.satellites_kiss_to_pdu_0, 'out'), (self.satellites_hdlc_framer_0, 'in'))
        self.connect((self.analog_nbfm_tx_0, 0), (self.interp_fir_filter_xxx_1, 0))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.interp_fir_filter_xxx_0, 0))
        self.connect((self.blocks_char_to_float_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_float_to_short_0, 0), (self.network_udp_sink_0, 0))
        self.connect((self.blocks_repeat_0, 0), (self.blocks_char_to_float_0, 0))
        self.connect((self.digital_scrambler_bb_0, 0), (self.blocks_repeat_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.analog_nbfm_tx_0, 0))
        self.connect((self.interp_fir_filter_xxx_0, 0), (self.blocks_float_to_short_0, 0))
        self.connect((self.interp_fir_filter_xxx_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.pdu_pdu_to_stream_x_0, 0), (self.satellites_kiss_to_pdu_0, 0))
        self.connect((self.pdu_pdu_to_tagged_stream_0, 0), (self.satellites_nrzi_encode_0, 0))
        self.connect((self.satellites_nrzi_encode_0, 0), (self.digital_scrambler_bb_0, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "AX25_Tx")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_multiplier(self):
        return self.multiplier

    def set_multiplier(self, multiplier):
        self.multiplier = multiplier
        self.set_samp_rate(self.data_rate*self.multiplier)
        self.blocks_repeat_0.set_interpolation(self.multiplier)

    def get_data_rate(self):
        return self.data_rate

    def set_data_rate(self, data_rate):
        self.data_rate = data_rate
        self.set_samp_rate(self.data_rate*self.multiplier)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate*self.rf_multiplier)

    def get_rf_multiplier(self):
        return self.rf_multiplier

    def set_rf_multiplier(self, rf_multiplier):
        self.rf_multiplier = rf_multiplier
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate*self.rf_multiplier)

    def get_freq(self):
        return self.freq

    def set_freq(self, freq):
        self.freq = freq
        self.uhd_usrp_sink_0.set_center_freq(self.freq, 0)




def main(top_block_cls=AX25_Tx, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
