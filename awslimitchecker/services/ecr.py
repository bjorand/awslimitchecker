"""
awslimitchecker/services/ecr.py

The latest version of this package is available at:
<https://github.com/jantman/awslimitchecker>

################################################################################
Copyright 2015-2018 Jason Antman <jason@jasonantman.com>

    This file is part of awslimitchecker, also known as awslimitchecker.

    awslimitchecker is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    awslimitchecker is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with awslimitchecker.  If not, see <http://www.gnu.org/licenses/>.

The Copyright and Authors attributions contained herein may not be removed or
otherwise altered, except to add the Author attribution of a contributor to
this work. (Additional Terms pursuant to Section 7b of the AGPL v3)
################################################################################
While not legally required, I sincerely request that anyone who finds
bugs please submit them at <https://github.com/jantman/awslimitchecker> or
to me via email, and that you send any contributions or improvements
either as a pull request on GitHub, or to me via email.
################################################################################

AUTHORS:
Benjamin Jorand <benjamin.jorand@gmail.com>
################################################################################
"""

import abc  # noqa
import logging

from .base import _AwsService
from ..limit import AwsLimit

logger = logging.getLogger(__name__)


class _EcrService(_AwsService):

    service_name = 'ECR'
    api_name = 'ecr'  # AWS API name to connect to (boto3.client)
    quotas_service_code = 'ecr'

    def find_usage(self):
        """
        Determine the current usage for each limit of this service,
        and update corresponding Limit via
        :py:meth:`~.AwsLimit._add_current_usage`.
        """
        logger.debug("Checking usage for service %s", self.service_name)
        self.connect()
        for lim in self.limits.values():
            lim._reset_usage()
        self.limits['Rate of BatchCheckLayerAvailability requests']._add_current_usage(
            self._get_cloudwatch_usage_latest(
                [
                    {'Name': 'Type', 'Value': 'API'},
                    {'Name': 'Resource', 'Value': 'BatchCheckLayerAvailability'},
                    {'Name': 'Service', 'Value': 'ECR'},
                    {'Name': 'Class', 'Value': 'None'},
                ],
                'CallCount',
                stat='Sum',
            ),
            aws_type='AWS::ECR::Repository'
        )
        self.limits['Rate of BatchGetImage requests']._add_current_usage(
            self._get_cloudwatch_usage_latest(
                [
                    {'Name': 'Type', 'Value': 'API'},
                    {'Name': 'Resource', 'Value': 'BatchGetImage'},
                    {'Name': 'Service', 'Value': 'ECR'},
                    {'Name': 'Class', 'Value': 'None'},
                ],
                'CallCount',
                stat='Sum',
            ),
            aws_type='AWS::ECR::Repository'
        )
        self.limits['Rate of CompleteLayerUpload requests']._add_current_usage(
            self._get_cloudwatch_usage_latest(
                [
                    {'Name': 'Type', 'Value': 'API'},
                    {'Name': 'Resource', 'Value': 'CompleteLayerUpload'},
                    {'Name': 'Service', 'Value': 'ECR'},
                    {'Name': 'Class', 'Value': 'None'},
                ],
                'CallCount',
                stat='Sum',
            ),
            aws_type='AWS::ECR::Repository'
        )
        self.limits['Rate of GetAuthorizationToken requests']._add_current_usage(
            self._get_cloudwatch_usage_latest(
                [
                    {'Name': 'Type', 'Value': 'API'},
                    {'Name': 'Resource', 'Value': 'GetAuthorizationToken'},
                    {'Name': 'Service', 'Value': 'ECR'},
                    {'Name': 'Class', 'Value': 'None'},
                ],
                'CallCount',
                stat='Sum',
            ),
            aws_type='AWS::ECR::Repository'
        )
        self.limits['Rate of GetDownloadUrlForLayer requests']._add_current_usage(
            self._get_cloudwatch_usage_latest(
                [
                    {'Name': 'Type', 'Value': 'API'},
                    {'Name': 'Resource', 'Value': 'GetDownloadUrlForLayer'},
                    {'Name': 'Service', 'Value': 'ECR'},
                    {'Name': 'Class', 'Value': 'None'},
                ],
                'CallCount',
                stat='Sum',
            ),
            aws_type='AWS::ECR::Repository'
        )
        self.limits['Rate of InitiateLayerUpload requests']._add_current_usage(
            self._get_cloudwatch_usage_latest(
                [
                    {'Name': 'Type', 'Value': 'API'},
                    {'Name': 'Resource', 'Value': 'InitiateLayerUpload'},
                    {'Name': 'Service', 'Value': 'ECR'},
                    {'Name': 'Class', 'Value': 'None'},
                ],
                'CallCount',
                stat='Sum',
            ),
            aws_type='AWS::ECR::Repository'
        )
        self.limits['Rate of PutImage requests']._add_current_usage(
            self._get_cloudwatch_usage_latest(
                [
                    {'Name': 'Type', 'Value': 'API'},
                    {'Name': 'Resource', 'Value': 'PutImage'},
                    {'Name': 'Service', 'Value': 'ECR'},
                    {'Name': 'Class', 'Value': 'None'},
                ],
                'CallCount',
                stat='Sum',
            ),
            aws_type='AWS::ECR::Repository'
        )
        self.limits['Rate of UploadLayerPart requests']._add_current_usage(
            self._get_cloudwatch_usage_latest(
                [
                    {'Name': 'Type', 'Value': 'API'},
                    {'Name': 'Resource', 'Value': 'UploadLayerPart'},
                    {'Name': 'Service', 'Value': 'ECR'},
                    {'Name': 'Class', 'Value': 'None'},
                ],
                'CallCount',
                stat='Sum',
            ),
            aws_type='AWS::ECR::Repository'
        )
        self._have_usage = True
        logger.debug("Done checking usage.")

    def get_limits(self):
        """
        Return all known limits for this service, as a dict of their names
        to :py:class:`~.AwsLimit` objects.

        :returns: dict of limit names to :py:class:`~.AwsLimit` objects
        :rtype: dict
        """
        if self.limits != {}:
            return self.limits
        limits = {}

        limits['Rate of BatchCheckLayerAvailability requests'] = AwsLimit(
            'Rate of BatchCheckLayerAvailability requests',
            self,
            200*60,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::ECR::Repository',
        )
        limits['Rate of BatchGetImage requests'] = AwsLimit(
            'Rate of BatchGetImage requests',
            self,
            2000*60,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::ECR::Repository',
        )
        limits['Rate of CompleteLayerUpload requests'] = AwsLimit(
            'Rate of CompleteLayerUpload requests',
            self,
            10*60,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::ECR::Repository',
        )
        limits['Rate of GetAuthorizationToken requests'] = AwsLimit(
            'Rate of GetAuthorizationToken requests',
            self,
            500*60,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::ECR::Repository',
        )
        limits['Rate of GetDownloadUrlForLayer requests'] = AwsLimit(
            'Rate of GetDownloadUrlForLayer requests',
            self,
            3000*60,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::ECR::Repository',
        )
        limits['Rate of InitiateLayerUpload requests'] = AwsLimit(
            'Rate of InitiateLayerUpload requests',
            self,
            10*60,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::ECR::Repository',
        )
        limits['Rate of PutImage requests'] = AwsLimit(
            'Rate of PutImage requests',
            self,
            10*60,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::ECR::Repository',
        )
        limits['Rate of UploadLayerPart requests'] = AwsLimit(
            'Rate of UploadLayerPart requests',
            self,
            260*60,
            self.warning_threshold,
            self.critical_threshold,
            limit_type='AWS::ECR::Repository',
        )
        self.limits = limits
        return limits
