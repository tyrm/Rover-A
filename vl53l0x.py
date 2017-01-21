#!/usr/bin/env python
from Adafruit_GPIO import I2C
import logging
import time

# Register Addresses
VL53L0X_REG_SYSRANGE_START = 0x00

VL53L0X_REG_SYSTEM_THRESH_HIGH = 0x0C
VL53L0X_REG_SYSTEM_THRESH_LOW = 0x0E

VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG = 0x01
VL53L0X_REG_SYSTEM_RANGE_CONFIG = 0x09
VL53L0X_REG_SYSTEM_INTERMEASUREMENT_PERIOD = 0x04

VL53L0X_REG_SYSTEM_INTERRUPT_CONFIG_GPIO = 0x0A

VL53L0X_REG_GPIO_HV_MUX_ACTIVE_HIGH = 0x84

VL53L0X_REG_SYSTEM_INTERRUPT_CLEAR = 0x0B

VL53L0X_REG_RESULT_INTERRUPT_STATUS = 0x13
VL53L0X_REG_RESULT_RANGE_STATUS = 0x14

VL53L0X_REG_RESULT_CORE_AMBIENT_WINDOW_EVENTS_RTN = 0xBC
VL53L0X_REG_RESULT_CORE_RANGING_TOTAL_EVENTS_RTN = 0xC0
VL53L0X_REG_RESULT_CORE_AMBIENT_WINDOW_EVENTS_REF = 0xD0
VL53L0X_REG_RESULT_CORE_RANGING_TOTAL_EVENTS_REF = 0xD4
VL53L0X_REG_RESULT_PEAK_SIGNAL_RATE_REF = 0xB6

VL53L0X_REG_ALGO_PART_TO_PART_RANGE_OFFSET_MM = 0x28

VL53L0X_REG_I2C_SLAVE_DEVICE_ADDRESS = 0x8A

VL53L0X_REG_MSRC_CONFIG_CONTROL = 0x60

VL53L0X_REG_PRE_RANGE_CONFIG_MIN_SNR = 0x27
VL53L0X_REG_PRE_RANGE_CONFIG_VALID_PHASE_LOW = 0x56
VL53L0X_REG_PRE_RANGE_CONFIG_VALID_PHASE_HIGH = 0x57
VL53L0X_REG_PRE_RANGE_MIN_COUNT_RATE_RTN_LIMIT = 0x64

VL53L0X_REG_FINAL_RANGE_CONFIG_MIN_SNR = 0x67
VL53L0X_REG_FINAL_RANGE_CONFIG_VALID_PHASE_LOW = 0x47
VL53L0X_REG_FINAL_RANGE_CONFIG_VALID_PHASE_HIGH = 0x48
VL53L0X_REG_FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT = 0x44

VL53L0X_REG_PRE_RANGE_CONFIG_SIGMA_THRESH_HI = 0x61
VL53L0X_REG_PRE_RANGE_CONFIG_SIGMA_THRESH_LO = 0x62

VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD = 0x50
VL53L0X_REG_PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI = 0x51
VL53L0X_REG_PRE_RANGE_CONFIG_TIMEOUT_MACROP_LO = 0x52

VL53L0X_REG_SYSTEM_HISTOGRAM_BIN = 0x81
VL53L0X_REG_HISTOGRAM_CONFIG_INITIAL_PHASE_SELECT = 0x33
VL53L0X_REG_HISTOGRAM_CONFIG_READOUT_CTRL = 0x55

VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD = 0x70
VL53L0X_REG_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI = 0x71
VL53L0X_REG_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_LO = 0x72
VL53L0X_REG_CROSSTALK_COMPENSATION_PEAK_RATE_MCPS = 0x20

VL53L0X_REG_MSRC_CONFIG_TIMEOUT_MACROP = 0x46

VL53L0X_REG_SOFT_RESET_GO2_SOFT_RESET_N = 0xBF
VL53L0X_REG_IDENTIFICATION_MODEL_ID = 0xC0
VL53L0X_REG_IDENTIFICATION_REVISION_ID = 0xC2

VL53L0X_REG_OSC_CALIBRATE_VAL = 0xF8

VL53L0X_REG_GLOBAL_CONFIG_VCSEL_WIDTH = 0x32
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_0 = 0xB0
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_1 = 0xB1
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_2 = 0xB2
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_3 = 0xB3
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_4 = 0xB4
VL53L0X_REG_GLOBAL_CONFIG_SPAD_ENABLES_REF_5 = 0xB5

VL53L0X_REG_GLOBAL_CONFIG_REF_EN_START_SELECT = 0xB6
VL53L0X_REG_DYNAMIC_SPAD_NUM_REQUESTED_REF_SPAD = 0x4E
VL53L0X_REG_DYNAMIC_SPAD_REF_EN_START_OFFSET = 0x4F
VL53L0X_REG_POWER_MANAGEMENT_GO1_POWER_FORCE = 0x80

VL53L0X_REG_VHV_CONFIG_PAD_SCL_SDA__EXTSUP_HV = 0x89

VL53L0X_REG_ALGO_PHASECAL_LIM = 0x30
VL53L0X_REG_ALGO_PHASECAL_CONFIG_TIMEOUT = 0x30

# Sequence Steps list
VL53L0X_SEQUENCESTEP_TCC = 0
VL53L0X_SEQUENCESTEP_DSS = 1
VL53L0X_SEQUENCESTEP_MSRC = 2
VL53L0X_SEQUENCESTEP_PRE_RANGE = 3
VL53L0X_SEQUENCESTEP_FINAL_RANGE = 4

# Check Enable list
VL53L0X_CHECKENABLE_SIGMA_FINAL_RANGE = 0
VL53L0X_CHECKENABLE_SIGNAL_RATE_FINAL_RANGE = 1
VL53L0X_CHECKENABLE_SIGNAL_REF_CLIP = 2
VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD = 3
VL53L0X_CHECKENABLE_SIGNAL_RATE_MSRC = 4
VL53L0X_CHECKENABLE_SIGNAL_RATE_PRE_RANGE = 5

# Vcsel Period
VL53L0X_VCSEL_PERIOD_PRE_RANGE = 0
VL53L0X_VCSEL_PERIOD_FINAL_RANGE = 1

logging.getLogger(__name__)


class VL53L0X:
    def __init__(self, address, i2c=None):
        if i2c is None:
            i2c = I2C
        pass

        self.device = i2c.get_i2c_device(address)

        rev_id = self.get_revision_id()
        dev_id = self.get_model_id()

        # Internal Parameters
        self.limit_checks_value = [0, 0, 0, 0, 0, 0]

        logging.info("VL53L0X RevisionID[{0}] DeviceID[{1}]".format(hex(rev_id), hex(dev_id)))

    def calc_macro_period_ps(self, vcsel_period_pclks):
        pll_period_ps = 1655
        macro_period_vclks = 2304

        return int(macro_period_vclks * vcsel_period_pclks * pll_period_ps)

    def calc_timeout_mclks(self, timeout_period_us, vcsel_period_pclks):
        macro_period_ps = self.calc_macro_period_ps(vcsel_period_pclks)
        macro_period_ns = (macro_period_ps + 500) / 1000

        return int(((timeout_period_us * 1000) + (macro_period_ns / 2)) / macro_period_ns)

    def calc_timeout_us(self, timeout_period_mclks, vcsel_period_pclks):
        macro_period_ps = self.calc_macro_period_ps(vcsel_period_pclks)
        macro_period_ns = (macro_period_ps + 500) / 1000

        return ((timeout_period_mclks * macro_period_ns) + 500) / 1000

    def decode_timeout(self, encoded_timeout):
        return (int(encoded_timeout & 0x00FF) << int((encoded_timeout & 0xFF00) >> 8)) + 1

    def decode_vcsel_period(self, vcsel_period_reg):
        """Converts the encoded VCSEL period register value into the real period in PLL clocks"""
        return (vcsel_period_reg + 1) << 1

    def encode_timeout(self, timeout_macro_clks):
        ms_byte = 0

        if timeout_macro_clks > 0:
            ls_byte = timeout_macro_clks - 1

            while (ls_byte & 0xFFFFFF00) > 0:
                ls_byte = ls_byte >> 1
                ms_byte += 1

            return (ms_byte << 8) + (ls_byte & 0x000000FF)
        else:
            return 0

    def fixpoint1616_to_fixpoint97(self, value):
        return int((value >> 9) & 0xFFFF)

    def get_sequence_step_enables(self):
        val = self.device.readU8(VL53L0X_REG_SYSTEM_SEQUENCE_CONFIG)

        enables = {}

        enables['TccOn'] = bool(self.sequence_step_enabled(VL53L0X_SEQUENCESTEP_TCC, val))
        enables['DssOn'] = bool(self.sequence_step_enabled(VL53L0X_SEQUENCESTEP_DSS, val))
        enables['MsrcOn'] = bool(self.sequence_step_enabled(VL53L0X_SEQUENCESTEP_MSRC, val))
        enables['PreRangeOn'] = bool(self.sequence_step_enabled(VL53L0X_SEQUENCESTEP_PRE_RANGE, val))
        enables['FinalRangeOn'] = bool(self.sequence_step_enabled(VL53L0X_SEQUENCESTEP_FINAL_RANGE, val))

        return enables

    def get_sequence_step_timeout(self, step_id):
        if step_id == VL53L0X_SEQUENCESTEP_TCC or step_id == VL53L0X_SEQUENCESTEP_DSS or step_id == VL53L0X_SEQUENCESTEP_MSRC:
            current_vcsel_pulse_period_p_clk = self.get_vcsel_pulse_period(VL53L0X_VCSEL_PERIOD_PRE_RANGE)
            encoded_time_out_byte = self.device.readU8(VL53L0X_REG_MSRC_CONFIG_TIMEOUT_MACROP)

            msrc_time_out_m_clks = self.decode_timeout(encoded_time_out_byte)
            return self.calc_timeout_us(msrc_time_out_m_clks, current_vcsel_pulse_period_p_clk)
        elif step_id == VL53L0X_SEQUENCESTEP_PRE_RANGE:
            current_vcsel_pulse_period_p_clk = self.get_vcsel_pulse_period(VL53L0X_VCSEL_PERIOD_PRE_RANGE)
            encoded_time_out_byte = self.device.readU16(VL53L0X_REG_PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI, False)

            msrc_time_out_m_clks = self.decode_timeout(encoded_time_out_byte)
            return self.calc_timeout_us(msrc_time_out_m_clks, current_vcsel_pulse_period_p_clk)
        elif step_id == VL53L0X_SEQUENCESTEP_FINAL_RANGE:
            scheduler_sequence_steps = self.get_sequence_step_enables()
            pre_range_time_out_m_clks = 0

            if scheduler_sequence_steps['PreRangeOn']:
                current_vcsel_pulse_period_p_clk = self.get_vcsel_pulse_period(VL53L0X_VCSEL_PERIOD_PRE_RANGE)
                pre_range_encoded_time_out = self.device.readU16(VL53L0X_REG_PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI, False)
                pre_range_time_out_m_clks = self.decode_timeout(pre_range_encoded_time_out)

            current_vcsel_pulse_period_p_clk = self.get_vcsel_pulse_period(VL53L0X_VCSEL_PERIOD_FINAL_RANGE)
            final_range_encoded_time_out = self.device.readU16(VL53L0X_REG_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI, False)
            final_range_time_out_m_clks = self.decode_timeout(final_range_encoded_time_out)

            final_range_time_out_m_clks -= pre_range_time_out_m_clks
            return self.calc_timeout_us(final_range_time_out_m_clks, current_vcsel_pulse_period_p_clk)
        else:
            raise ValueError("get_sequence_step_timeout received invalid step_id")

    def get_vcsel_pulse_period(self, period_type):
        if period_type == VL53L0X_VCSEL_PERIOD_PRE_RANGE:
            vcsel_period_reg = self.device.readU8(VL53L0X_REG_PRE_RANGE_CONFIG_VCSEL_PERIOD)
        elif period_type == VL53L0X_VCSEL_PERIOD_FINAL_RANGE:
            vcsel_period_reg = self.device.readU8(VL53L0X_REG_FINAL_RANGE_CONFIG_VCSEL_PERIOD)
        else:
            raise ValueError("get_vcsel_pulse_period received invalid period_type")

        return self.decode_vcsel_period(vcsel_period_reg)

    def sequence_step_enabled(self, step_id, val):
        if step_id == VL53L0X_SEQUENCESTEP_TCC:
            return (val & 0x10) >> 4
        elif step_id == VL53L0X_SEQUENCESTEP_DSS:
            return (val & 0x08) >> 3
        elif step_id == VL53L0X_SEQUENCESTEP_MSRC:
            return (val & 0x04) >> 2
        elif step_id == VL53L0X_SEQUENCESTEP_PRE_RANGE:
            return (val & 0x40) >> 6
        elif step_id == VL53L0X_SEQUENCESTEP_FINAL_RANGE:
            return (val & 0x80) >> 7
        else:
            raise ValueError("sequence_step_enabled received invalid step_id")

    def set_limit_check_value(self, limit_check_id, limit_check_value):
        if limit_check_id == VL53L0X_CHECKENABLE_SIGMA_FINAL_RANGE:
            self.limit_checks_value[VL53L0X_CHECKENABLE_SIGMA_FINAL_RANGE] = limit_check_value
        elif limit_check_id == VL53L0X_CHECKENABLE_SIGNAL_RATE_FINAL_RANGE:
            self.device.write16(VL53L0X_REG_FINAL_RANGE_CONFIG_MIN_COUNT_RATE_RTN_LIMIT,
                                self.fixpoint1616_to_fixpoint97(limit_check_value))
        elif limit_check_id == VL53L0X_CHECKENABLE_SIGNAL_REF_CLIP:
            self.limit_checks_value[VL53L0X_CHECKENABLE_SIGNAL_REF_CLIP] = limit_check_value
        elif limit_check_id == VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD:
            self.limit_checks_value[VL53L0X_CHECKENABLE_RANGE_IGNORE_THRESHOLD] = limit_check_value
        elif limit_check_id == VL53L0X_CHECKENABLE_SIGNAL_RATE_MSRC or limit_check_id == VL53L0X_CHECKENABLE_SIGNAL_RATE_PRE_RANGE:
            self.device.write16(VL53L0X_REG_PRE_RANGE_MIN_COUNT_RATE_RTN_LIMIT,
                                self.fixpoint1616_to_fixpoint97(limit_check_value))
        else:
            raise ValueError("sequence_step_enabled received invalid step_id")

    def set_measurement_timing_budget_micro_seconds(self, measurement_timing_budget_micro_seconds):
        start_overhead_micro_seconds = 1910
        end_overhead_micro_seconds = 960
        msrc_overhead_micro_seconds = 660
        tcc_overhead_micro_seconds = 590
        dss_overhead_micro_seconds = 690
        pre_range_overhead_micro_seconds = 660
        final_range_overhead_micro_seconds = 550
        c_min_timing_budget_micro_seconds = 20000

        if measurement_timing_budget_micro_seconds < c_min_timing_budget_micro_seconds:
            measurement_timing_budget_micro_seconds = c_min_timing_budget_micro_seconds

        final_range_timing_budget_micro_seconds = measurement_timing_budget_micro_seconds - (
            start_overhead_micro_seconds + end_overhead_micro_seconds)

        sequence_steps = self.get_sequence_step_enables()

        if sequence_steps['TccOn'] or sequence_steps['MsrcOn'] or sequence_steps['DssOn']:
            msrc_dcc_tcc_timeout_micro_seconds = self.get_sequence_step_timeout(VL53L0X_SEQUENCESTEP_MSRC)

            if sequence_steps['TccOn']:
                sub_timeout = msrc_dcc_tcc_timeout_micro_seconds + tcc_overhead_micro_seconds

                if sub_timeout < final_range_timing_budget_micro_seconds:
                    final_range_timing_budget_micro_seconds -= sub_timeout
                else:
                    raise ValueError("Requested timeout too big.")

            if sequence_steps['DssOn']:
                sub_timeout = 2 * (msrc_dcc_tcc_timeout_micro_seconds + dss_overhead_micro_seconds)

                if sub_timeout < final_range_timing_budget_micro_seconds:
                    final_range_timing_budget_micro_seconds -= sub_timeout
                else:
                    raise ValueError("Requested timeout too big.")

            elif sequence_steps['MsrcOn']:
                sub_timeout = msrc_dcc_tcc_timeout_micro_seconds + msrc_overhead_micro_seconds

                if sub_timeout < final_range_timing_budget_micro_seconds:
                    final_range_timing_budget_micro_seconds -= sub_timeout
                else:
                    raise ValueError("Requested timeout too big.")

        if sequence_steps['PreRangeOn']:
            pre_range_timeout_micro_seconds = self.get_sequence_step_timeout(VL53L0X_SEQUENCESTEP_PRE_RANGE)

            sub_timeout = pre_range_timeout_micro_seconds + pre_range_overhead_micro_seconds

            if sub_timeout < final_range_timing_budget_micro_seconds:
                final_range_timing_budget_micro_seconds -= sub_timeout
            else:
                raise ValueError("Requested timeout too big.")

        if sequence_steps['FinalRangeOn']:
            final_range_timing_budget_micro_seconds -= final_range_overhead_micro_seconds

        self.set_sequence_step_timeout(VL53L0X_SEQUENCESTEP_FINAL_RANGE, final_range_timing_budget_micro_seconds)

    def set_sequence_step_timeout(self, step_id, TimeOutMicroSecs):
        if step_id == VL53L0X_SEQUENCESTEP_TCC or step_id == VL53L0X_SEQUENCESTEP_DSS or step_id == VL53L0X_SEQUENCESTEP_MSRC:
            current_vcsel_pulse_period_p_clk = self.get_vcsel_pulse_period(VL53L0X_VCSEL_PERIOD_PRE_RANGE)
            msrc_range_time_out_m_clks = self.calc_timeout_mclks(TimeOutMicroSecs, current_vcsel_pulse_period_p_clk)

            if msrc_range_time_out_m_clks > 256:
                msrc_encoded_time_out = 255
            else:
                msrc_encoded_time_out = msrc_range_time_out_m_clks - 1

            self.device.write8(VL53L0X_REG_MSRC_CONFIG_TIMEOUT_MACROP, msrc_encoded_time_out)
        elif step_id == VL53L0X_SEQUENCESTEP_PRE_RANGE:
            current_vcsel_pulse_period_p_clk = self.get_vcsel_pulse_period(VL53L0X_VCSEL_PERIOD_PRE_RANGE)
            pre_range_time_out_m_clks = self.calc_timeout_mclks(TimeOutMicroSecs, current_vcsel_pulse_period_p_clk)
            pre_range_encoded_time_out = self.encode_timeout(pre_range_time_out_m_clks)

            self.device.write16(VL53L0X_REG_PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI, pre_range_encoded_time_out)
        elif step_id == VL53L0X_SEQUENCESTEP_FINAL_RANGE:
            sequence_steps = self.get_sequence_step_enables()
            pre_range_time_out_m_clks = 0
            if sequence_steps['PreRangeOn']:
                current_vcsel_pulse_period_p_clk = self.get_vcsel_pulse_period(VL53L0X_VCSEL_PERIOD_PRE_RANGE)
                pre_range_encoded_time_out = self.device.readU16(VL53L0X_REG_PRE_RANGE_CONFIG_TIMEOUT_MACROP_HI, False)
                pre_range_time_out_m_clks = self.decode_timeout(pre_range_encoded_time_out)

            current_vcsel_pulse_period_p_clk = self.get_vcsel_pulse_period(VL53L0X_VCSEL_PERIOD_FINAL_RANGE)
            final_range_time_out_m_clks = self.calc_timeout_mclks(TimeOutMicroSecs, current_vcsel_pulse_period_p_clk)
            final_range_time_out_m_clks += pre_range_time_out_m_clks
            final_range_encoded_time_out = self.encode_timeout(final_range_time_out_m_clks)

            self.device.write16(VL53L0X_REG_FINAL_RANGE_CONFIG_TIMEOUT_MACROP_HI, final_range_encoded_time_out)
        else:
            raise ValueError("get_sequence_step_timeout received invalid step_id")

    # custom
    def get_model_id(self):
        return self.device.readU8(VL53L0X_REG_IDENTIFICATION_MODEL_ID)

    def get_result_range_status(self):
        return self.device.readU8(VL53L0X_REG_RESULT_RANGE_STATUS)

    def get_result_range_ambient(self):
        return self.device.readU16(VL53L0X_REG_RESULT_RANGE_STATUS + 6, False)

    def get_result_range_signal_count(self):
        return self.device.readU16(VL53L0X_REG_RESULT_RANGE_STATUS + 8, False)

    def get_result_range_disance(self):
        return self.device.readU16(VL53L0X_REG_RESULT_RANGE_STATUS + 10, False)

    def get_revision_id(self):
        return self.device.readU8(VL53L0X_REG_IDENTIFICATION_REVISION_ID)

    def measure_distance(self):
        self.set_sysrange_start(0x01)

        cnt = 0
        while (cnt < 100):  # 1 second waiting time max
            time.sleep(0.010)
            val = self.get_result_range_status()
            if (val & 0x01):
                break
            cnt += 1

        if not (val & 0x01):
            logging.warn("VL53L0X scanner not ready")

        return [self.get_result_range_disance(), self.get_result_range_signal_count()]

    def set_sysrange_start(self, val):
        val = val & 0xFF
        self.device.write8(VL53L0X_REG_SYSRANGE_START, val)
