#!/usr/bin/env python3

# Copyright 2022 Shadow Robot Company Ltd.
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation version 2 of the License.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program. If not, see <http://www.gnu.org/licenses/>.

import rospy
from sr_hand_health_report_check import SrHealthReportCheck
from diagnostic_msgs.msg import DiagnosticArray


class MotorCheck(SrHealthReportCheck):
    def __init__(self, hand_side, fingers_to_test):
        super().__init__(hand_side, fingers_to_test)
        self._topic_name = '/diagnostics_agg'

    def run_check(self):
        result = {"motor_check": []}

        try:
            received_msg = rospy.wait_for_message(self._topic_name, DiagnosticArray, 5)
        except rospy.ROSException:
            rospy.logerr(f"Did not receive any message on {self._topic_name} topic")
            return result

        for message in received_msg.status:
            for item in message.values:
                if "SRDMotor" in item.key and self._hand_prefix in item.key:
                    split_motor_description_line = item.key.split(' ')
                    motor_name = f"{split_motor_description_line[0]}_{split_motor_description_line[-1]}".lower()
                    working_state = True
                    if item.value == "Motor error":
                        working_state = False
                    result['motor_check'].append(dict({motor_name: working_state}))
        return result
