import asyncio
import json

import requests
import urllib3
from walkoff_app_sdk.app_base import AppBase

class Crowdstrike_Falcon(AppBase):

    __version__ = "1.0"
    app_name = "Crowdstrike_Falcon"


    def __init__(self, redis, logger, console_logger=None):
        self.verify = False
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        super().__init__(redis, logger, console_logger)


    def setup_headers(self, headers):
        request_headers={}

        if len(headers) > 0:
            for header in headers.split("\n"):
                if '=' in header:
                    headersplit=header.split('=')
                    request_headers[headersplit[0].strip()] = headersplit[1].strip()
                elif ':' in header:
                    headersplit=header.split(':')
                    request_headers[headersplit[0].strip()] = headersplit[1].strip()
        return request_headers


    def setup_params(self, queries):
        params={}

        if len(queries) > 0:
            for query in queries.split("\&"):
                if '=' in query:
                    headersplit=query.split('&')
                    params[headersplit[0].strip()] = headersplit[1].strip()

        return params


    def generate_oauth2_access_token(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/oauth2/token"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)
        body={'client_id': client_id, 'client_secret': client_secret}
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def revoke_oauth2_access_token(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/oauth2/revoke"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)
        body={'client_id': client_id, 'client_secret': client_secret}
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def download_analysis_artifacts(self, url, client_id, client_secret, id, headers="", queries="", name=""):
        params={}
        request_headers={}
        url=f"{url}/falconx/entities/artifacts/v1?id={id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)


        if name:
            params["name"] = name
        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_detect_aggregates(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/detects/aggregates/detects/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def view_information_about_detections(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/detects/entities/summaries/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def modify_detections(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/detects/entities/detects/v2"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_sandbox_reports(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/falconx/queries/reports/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)


        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_rules_by_id(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/entities/rules/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_rules_from_a_rule_group_by_id(self, url, client_id, client_secret, rule_group_id, ids, headers="", queries="", comment=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/entities/rules/v1?rule_group_id={rule_group_id}&ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_a_rule_within_a_rule_group(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/ioarules/entities/rules/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_rules_within_a_rule_group(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/ioarules/entities/rules/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_prevention_policy_members(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/prevention-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def set_precedence_of_device_control_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/device-control-precedence/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_hidden_hosts(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter=""):
        params={}
        request_headers={}
        url=f"{url}/devices/queries/devices-hidden/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_rule_types_by_id(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/entities/rule-types/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_all_platform_ids(self, url, client_id, client_secret, headers="", queries="", offset="", limit=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/queries/platforms/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_combined_for_indicators(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/iocs/combined/indicator/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def set_precedence_of_response_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/response-precedence/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_set_of_sensor_visibility_exclusions(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sv-exclusions/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_the_sensor_visibility_exclusions_by_id(self, url, client_id, client_secret, ids, headers="", queries="", comment=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sv-exclusions/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_the_sensor_visibility_exclusions(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sv-exclusions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_the_sensor_visibility_exclusions(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sv-exclusions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_prevention_policy_ids(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/prevention/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_notifications_based_on_their_ids(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/recon/entities/notifications/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_notifications_based_on_ids_notifications(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/recon/entities/notifications/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_notification_status_or_assignee(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/recon/entities/notifications/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_sensor_installer_ids_by_provided_query(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter=""):
        params={}
        request_headers={}
        url=f"{url}/sensors/queries/installers/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_info_about_indicators(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter="", q="", include_deleted=""):
        params={}
        request_headers={}
        url=f"{url}/intel/combined/indicators/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q
        if include_deleted:
            params["include_deleted"] = include_deleted

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def download_earlier_rule_sets(self, url, client_id, client_secret, id, headers="", queries="", format=""):
        params={}
        request_headers={"Accept": "undefined"}
        url=f"{url}/intel/entities/rules-files/v1?id={id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_report_ids(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter="", q=""):
        params={}
        request_headers={}
        url=f"{url}/intel/queries/reports/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_rule_ids(self, url, client_id, client_secret, type, headers="", queries="", offset="", limit="", sort="", name="", description="", tags="", min_created_date="", max_created_date="", q=""):
        params={}
        request_headers={}
        url=f"{url}/intel/queries/rules/v1?type={type}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if name:
            params["name"] = name
        if description:
            params["description"] = description
        if tags:
            params["tags"] = tags
        if min_created_date:
            params["min_created_date"] = min_created_date
        if max_created_date:
            params["max_created_date"] = max_created_date
        if q:
            params["q"] = q

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_sensor_update_policies(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/sensor-update/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_set_of_ioa_exclusions(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/ioa-exclusions/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_the_ioa_exclusions_by_id(self, url, client_id, client_secret, ids, headers="", queries="", comment=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/ioa-exclusions/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_the_ioa_exclusions(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/ioa-exclusions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_the_ioa_exclusions(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/ioa-exclusions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_sensor_update_policy_member_ids(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/sensor-update-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_sensor_visibility_exclusions(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/sv-exclusions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def find_ids_for_submitted_scans(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/scanner/queries/scans/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_sensor_installer_details_by_provided_query(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter=""):
        params={}
        request_headers={}
        url=f"{url}/sensors/combined/installers/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_hosts(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter=""):
        params={}
        request_headers={}
        url=f"{url}/devices/queries/devices-scroll/v1"

        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)


        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_info_about_reports(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter="", q="", fields=""):
        params={}
        request_headers={}
        url=f"{url}/intel/combined/reports/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q
        if fields:
            params["fields"] = fields

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_zipped_sample(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/malquery/entities/samples-fetch/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def schedule_samples_for_download(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/malquery/entities/samples-multidownload/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def perform_action_on_the_sensor_update_policies(self, url, client_id, client_secret, action_name, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sensor-update-actions/v1?action_name={action_name}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def query_notifications(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter="", q=""):
        params={}
        request_headers={}
        url=f"{url}/recon/queries/notifications/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_prevention_policies(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/prevention/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_status_of_an_executed_active_responder_command_on_a_single_host(self, url, client_id, client_secret, cloud_request_id, sequence_id, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/active-responder-command/v1?cloud_request_id={cloud_request_id}&sequence_id={sequence_id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def execute_an_active_responder_command_on_a_single_host(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/active-responder-command/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def find_all_rule_ids(self, url, client_id, client_secret, headers="", queries="", sort="", filter="", q="", offset="", limit=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/queries/rules/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def set_precedence_of_prevention_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/prevention-precedence/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_indicators_ids(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter="", q="", include_deleted=""):
        params={}
        request_headers={}
        url=f"{url}/intel/queries/indicators/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q
        if include_deleted:
            params["include_deleted"] = include_deleted

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_sensor_update_policy_members(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/sensor-update-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def batch_refresh_a_rtr_session_on_multiple_hosts_rtr_sessions_will_expire_after_10_minutes_unless_refreshed(self, url, client_id, client_secret, headers="", queries="", timeout="", timeout_duration="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/combined/batch-refresh-session/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if timeout_duration:
            params["timeout_duration"] = timeout_duration
        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_queued_session_metadata_by_session_id(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/queued-sessions/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def perform_action_on_the_device_control_policies(self, url, client_id, client_secret, action_name, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/device-control-actions/v1?action_name={action_name}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_scans_aggregations(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/scanner/aggregates/scans/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_detailed_notifications_based_on_their_ids(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/recon/entities/notifications-detailed-translated/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_specific_indicators_using_their_indicator_ids(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/intel/entities/indicators/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def find_all_rule_group_ids(self, url, client_id, client_secret, headers="", queries="", sort="", filter="", q="", offset="", limit=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/queries/rule-groups/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_falcon_malquery(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/malquery/queries/exact-search/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_available_builds_for_use_with_sensor_update_policies(self, url, client_id, client_secret, headers="", queries="", platform=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/sensor-update-builds/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_firewall_policies(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/firewall/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_set_of_host_groups(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/devices/entities/host-groups/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_set_of_host_groups(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/devices/entities/host-groups/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_host_groups(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/devices/entities/host-groups/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_host_groups(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/devices/entities/host-groups/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_behaviors(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/incidents/queries/behaviors/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_incidents(self, url, client_id, client_secret, headers="", queries="", sort="", filter="", offset="", limit=""):
        params={}
        request_headers={}
        url=f"{url}/incidents/queries/incidents/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_rule_groups_by_id(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/entities/rule-groups/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_rule_groups_by_id(self, url, client_id, client_secret, ids, headers="", queries="", comment=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/entities/rule-groups/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_a_rule_group(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/ioarules/entities/rule-groups/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_a_rule_group(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/ioarules/entities/rule-groups/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_all_rule_type_ids(self, url, client_id, client_secret, headers="", queries="", offset="", limit=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/queries/rule-types/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_information_about_search_and_download_quotas(self, url, client_id, client_secret, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/malquery/aggregates/quotas/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def refresh_a_session_timeout_on_a_single_host(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/refresh-session/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def query_crowdscore(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/incidents/combined/crowdscores/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def perform_actions_on_incidents(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/incidents/entities/incident-actions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_info_about_actors(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter="", q="", fields=""):
        params={}
        request_headers={}
        url=f"{url}/intel/combined/actors/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q
        if fields:
            params["fields"] = fields

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_response_policy_members(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/response-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def batch_initialize_a_rtr_session_on_multiple_hosts__before_any_rtr_commands_can_be_used_an_active_session_is_needed_on_the_host(self, url, client_id, client_secret, headers="", queries="", timeout="", timeout_duration="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/combined/batch-init-session/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if timeout_duration:
            params["timeout_duration"] = timeout_duration
        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_rtr_extracted_file_contents_for_specified_session_and_sha256(self, url, client_id, client_secret, session_id, sha256, headers="", queries="", filename=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/extracted-file-contents/v1?session_id={session_id}&sha256={sha256}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_host_groups(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/devices/combined/host-groups/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_all_pattern_severity_ids(self, url, client_id, client_secret, headers="", queries="", offset="", limit=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/queries/pattern-severities/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_indicators_by_ids(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/iocs/entities/indicators/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_indicators_by_ids(self, url, client_id, client_secret, headers="", queries="", filter="", ids="", comment=""):
        params={}
        request_headers={}
        url=f"{url}/iocs/entities/indicators/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if ids:
            params["ids"] = ids
        if comment:
            params["comment"] = comment

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_indicators(self, url, client_id, client_secret, headers="", queries="", retrodetects="", ignore_warnings="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/jsonX-CS-USERNAME"}
        url=f"{url}/iocs/entities/indicators/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if ignore_warnings:
            params["ignore_warnings"] = ignore_warnings
        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_indicators(self, url, client_id, client_secret, headers="", queries="", retrodetects="", ignore_warnings="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/jsonX-CS-USERNAME"}
        url=f"{url}/iocs/entities/indicators/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if ignore_warnings:
            params["ignore_warnings"] = ignore_warnings
        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_a_set_of_device_control_policies(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/device-control/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_a_set_of_device_control_policies(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/device-control/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_device_control_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/device-control/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_device_control_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/device-control/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_ioa_exclusions(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/ioa-exclusions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_aggregates_on_session_data(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/aggregates/sessions/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_a_session(self, url, client_id, client_secret, session_id, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/sessions/v1?session_id={session_id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def initialize_a_new_session_with_the_rtr_cloud(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/sessions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_full_sandbox_report(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/falconx/entities/reports/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_report(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/falconx/entities/reports/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_ml_exclusions(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/ml-exclusions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_sensor_update_policy_ids(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/sensor-update/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_a_queued_session_command(self, url, client_id, client_secret, session_id, cloud_request_id, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/queued-sessions/command/v1?session_id={session_id}&cloud_request_id={cloud_request_id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def preview_rules_notification_count_and_distribution(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/recon/aggregates/rules-preview/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_report_pdf_attachment(self, url, client_id, client_secret, id, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/intel/entities/report-files/v1?id={id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_a_set_of_prevention_policies(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/prevention/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_a_set_of_prevention_policies(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/prevention/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_prevention_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/prevention/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_prevention_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/prevention/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_putfiles_based_on_the_ids_given(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/put-files/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_a_putfile_based_on_the_ids_given(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/put-files/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def upload_a_new_putfile_to_use_for_the_rtr_put_command(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/put-files/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_list_of_session_ids(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/queries/sessions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_list_of_samples(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/jsonX-CS-USERUUID"}
        url=f"{url}/samples/queries/samples/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def check_status_of_sandbox_analysis(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/falconx/entities/submissions/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def submit_upload_for_sandbox_analysis(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/falconx/entities/submissions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_number_of_hosts_that_have_observed_a_given_custom_ioc(self, url, client_id, client_secret, type, value, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/indicators/aggregates/devices-count/v1?type={type}&value={value}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def set_precedence_of_firewall_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/firewall-precedence/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_notification_aggregates(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/recon/aggregates/notifications/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_actions_based_on_their_ids(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/recon/entities/actions/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_an_action_from_a_monitoring_rule_based_on_the_action_id(self, url, client_id, client_secret, id, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/recon/entities/actions/v1?id={id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_actions_for_a_monitoring_rule(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/recon/entities/actions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_an_action_for_a_monitoring_rule(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/recon/entities/actions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def query_actions(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter="", q=""):
        params={}
        request_headers={}
        url=f"{url}/recon/queries/actions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_host_group_ids(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/devices/queries/host-groups/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_indexed_files_metadata_by_their_hash(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/malquery/entities/metadata/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_sensor_update_policies_with_additional_support_for_uninstall_protection(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/sensor-update/v2"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def perform_action_on_the_firewall_policies(self, url, client_id, client_secret, action_name, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/firewall-actions/v1?action_name={action_name}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_process_details(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/processes/entities/processes/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_short_summary_version_of_a_sandbox_report(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/falconx/entities/report-summaries/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def schedule_a_yara_based_search_for_execution(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/malquery/queries/hunt/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_the_status_of_batch_get_command__will_return_successful_files_when_they_are_finished_processing(self, url, client_id, client_secret, batch_get_cmd_req_id, headers="", queries="", timeout="", timeout_duration=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/combined/batch-get-command/v1?batch_get_cmd_req_id={batch_get_cmd_req_id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if timeout_duration:
            params["timeout_duration"] = timeout_duration

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def batch_executes_get_command_across_hosts_to_retrieve_files_after_this_call_is_made_get_realtimeresponsecombinedbatchgetcommandv1_is_used_to_query_for_the_results(self, url, client_id, client_secret, headers="", queries="", timeout="", timeout_duration="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/combined/batch-get-command/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if timeout_duration:
            params["timeout_duration"] = timeout_duration
        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def query_monitoring_rules(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter="", q=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/recon/queries/rules/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_sensor_installer_details_by_provided_sha256_ids(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/sensors/entities/installers/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def modify_host_tags(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/devices/entities/devices/tags/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_response_policy_member_ids(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/response-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_status_of_an_executed_rtr_administrator_command_on_a_single_host(self, url, client_id, client_secret, cloud_request_id, sequence_id, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/admin-command/v1?cloud_request_id={cloud_request_id}&sequence_id={sequence_id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def execute_a_rtr_administrator_command_on_a_single_host(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/admin-command/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def refresh_an_active_event_stream(self, url, client_id, client_secret, action_name, appId, partition, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/sensors/entities/datafeed-actions/v1/{partition}?action_name={action_name}&appId={appId}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def validates_field_values_and_checks_for_string_matches(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/ioarules/entities/rules/validate/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def check_the_status_of_a_volume_scan(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/scanner/entities/scans/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def submit_a_volume_of_files_for_ml_scanning(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/scanner/entities/scans/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def download_the_latest_rule_set(self, url, client_id, client_secret, type, headers="", queries="", format=""):
        params={}
        request_headers={"Accept": "undefined"}
        url=f"{url}/intel/entities/rules-latest-files/v1?type={type}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_rules_by_id(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/ioarules/entities/rules/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def find_all_rule_groups(self, url, client_id, client_secret, headers="", queries="", sort="", filter="", q="", offset="", limit=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/queries/rule-groups-full/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def check_the_status_and_results_of_an_asynchronous_request(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/malquery/entities/requests/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_set_of_ml_exclusions(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/ml-exclusions/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_the_ml_exclusions_by_id(self, url, client_id, client_secret, ids, headers="", queries="", comment=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/ml-exclusions/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_the_ml_exclusions(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/ml-exclusions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_the_ml_exclusions(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/ml-exclusions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_device_control_policy_ids(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/device-control/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_firewall_policy_member_ids(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/firewall-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_notifications_based_on_their_ids(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/recon/entities/notifications-translated/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_host_group_members(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/devices/combined/host-group-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_platforms_by_id(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/entities/platforms/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def perform_action_on_the_response_policies(self, url, client_id, client_secret, action_name, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/response-actions/v1?action_name={action_name}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_a_set_of_response_policies(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/response/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_a_set_of_response_policies(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/response/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_response_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/response/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_response_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/response/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def batch_executes_a_rtr_readonly_command(self, url, client_id, client_secret, headers="", queries="", timeout="", timeout_duration="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/combined/batch-command/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if timeout_duration:
            params["timeout_duration"] = timeout_duration
        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_session_metadata_by_session_id(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/sessions/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def perform_action_on_host_group(self, url, client_id, client_secret, action_name, host_group_id, hostnames, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/devices/entities/host-group-actions/v1?action_name={action_name}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        body = {"action_parameters": [{"name": "filter", "value": "(hostname:['" + hostnames + "'])" } ], "ids": [ host_group_id ]}
        ret = requests.post(url, headers=request_headers, params=params, json=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_device_control_policy_members(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/device-control-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_firewall_policies(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/firewall/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_a_set_of_sensor_update_policies_with_additional_support_for_uninstall_protection(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sensor-update/v2?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_sensor_update_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sensor-update/v2"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_sensor_update_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sensor-update/v2"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_list_of_putfile_ids(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/queries/put-files/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_list_of_custom_script_ids(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/queries/scripts/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_detailed_notifications_based_on_their_ids_with_raw_intelligence_content_that_generated_the_match(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/recon/entities/notifications-detailed/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_all_event_streams(self, url, client_id, client_secret, appId, headers="", queries="", format=""):
        params={}
        request_headers={}
        url=f"{url}/sensors/entities/datafeed/v2?appId={appId}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def download_sensor_installer_by_sha256_id(self, url, client_id, client_secret, id, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/sensors/entities/download-installer/v1?id={id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_hosts_that_have_observed_a_given_custom_ioc(self, url, client_id, client_secret, type, value, headers="", queries="", limit="", offset=""):
        params={}
        request_headers={}
        url=f"{url}/indicators/queries/devices/v1?type={type}&value={value}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_details_for_rule_sets_for_ids(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/intel/entities/rules/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def download_a_file_indexed_by_malquery(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/malquery/entities/download-files/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_an_uninstall_token_for_a_specific_device(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/reveal-uninstall-token/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_response_policy_ids(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/response/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_a_list_of_files_for_rtr_session(self, url, client_id, client_secret, session_id, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/file/v1?session_id={session_id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_a_rtr_session_file(self, url, client_id, client_secret, ids, session_id, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/file/v1?ids={ids}&session_id={session_id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_custom_scripts_based_on_the_ids_given(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/scripts/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_a_custom_script_based_on_the_id_given(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/scripts/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def upload_a_new_custom_script_to_use(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/scripts/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def upload_a_new_scripts_to_replace_an_existing_one(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/scripts/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_details_on_hosts(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/devices/entities/devices/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_actor_ids(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter="", q=""):
        params={}
        request_headers={}
        url=f"{url}/intel/queries/actors/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_ccid_to_use_with_sensor_installers(self, url, client_id, client_secret, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/sensors/queries/installers/ccid/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def find_submission_ids_for_uploaded_files(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/falconx/queries/submissions/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_details_on_behaviors(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/incidents/entities/behaviors/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_device_control_policies(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/device-control/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_prevention_policy_member_ids(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/prevention-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_status_of_an_executed_command_on_a_single_host(self, url, client_id, client_secret, cloud_request_id, sequence_id, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/command/v1?cloud_request_id={cloud_request_id}&sequence_id={sequence_id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def execute_a_command_on_a_single_host(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/entities/command/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_the_file_associated_with_the_given_id_sha256(self, url, client_id, client_secret, ids, headers="", queries="", password_protected=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/samples/entities/samples/v3?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_sample_from_the_collection(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/samples/entities/samples/v3?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def upload_a_file_for_further_cloud_analysis(self, url, client_id, client_secret, file_name, headers="", queries="", comment="", is_confidential="", body=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/samples/entities/samples/v3?file_name={file_name}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if is_confidential:
            params["is_confidential"] = is_confidential
        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_response_policies(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/response/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_a_set_of_firewall_policies(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/firewall/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_a_set_of_firewall_policies(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/firewall/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_firewall_policies(self, url, client_id, client_secret, headers="", queries="", clone_id="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/firewall/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_firewall_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/firewall/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def set_precedence_of_sensor_update_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sensor-update-precedence/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_device_control_policy_member_ids(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/queries/device-control-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def batch_executes_a_rtr_active_responder_command(self, url, client_id, client_secret, headers="", queries="", timeout="", timeout_duration="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/combined/batch-active-responder-command/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if timeout_duration:
            params["timeout_duration"] = timeout_duration
        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def batch_executes_a_rtr_administrator_command(self, url, client_id, client_secret, headers="", queries="", timeout="", timeout_duration="", body=""):
        params={}
        request_headers={}
        url=f"{url}/real-time-response/combined/batch-admin-command/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if timeout_duration:
            params["timeout_duration"] = timeout_duration
        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_monitoring_rules_rules_by_provided_ids(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/recon/entities/rules/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_monitoring_rules(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/recon/entities/rules/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_monitoring_rules(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/recon/entities/rules/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_monitoring_rules(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/recon/entities/rules/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_detection_ids(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter="", q=""):
        params={}
        request_headers={}
        url=f"{url}/detects/queries/detects/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter
        if q:
            params["q"] = q

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_the_file_associated_with_the_given_id_sha256(self, url, client_id, client_secret, ids, headers="", queries="", password_protected=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/samples/entities/samples/v2?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def upload_for_sandbox_analysis(self, url, client_id, client_secret, file_name, headers="", queries="", comment="", is_confidential="", body=""):
        params={}
        request_headers={"X-CS-USERUUID": "undefined"}
        url=f"{url}/samples/entities/samples/v2?file_name={file_name}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if is_confidential:
            params["is_confidential"] = is_confidential
        body = " ".join(body.strip().split()).encode("utf-8")
        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_host_group_member_ids(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/devices/queries/host-group-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_details_on_incidents(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/incidents/entities/incidents/GET/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_processes_associated_with_a_custom_ioc(self, url, client_id, client_secret, type, value, device_id, headers="", queries="", limit="", offset=""):
        params={}
        request_headers={}
        url=f"{url}/indicators/queries/processes/v1?type={type}&value={value}&device_id={device_id}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_specific_reports_using_their_report_ids(self, url, client_id, client_secret, ids, headers="", queries="", fields=""):
        params={}
        request_headers={}
        url=f"{url}/intel/entities/reports/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_indicators(self, url, client_id, client_secret, headers="", queries="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/iocs/queries/indicators/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_firewall_policy_members(self, url, client_id, client_secret, headers="", queries="", id="", filter="", offset="", limit="", sort=""):
        params={}
        request_headers={}
        url=f"{url}/policy/combined/firewall-members/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if filter:
            params["filter"] = filter
        if offset:
            params["offset"] = offset
        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def perform_action_on_the_prevention_policies(self, url, client_id, client_secret, action_name, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/prevention-actions/v1?action_name={action_name}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_a_set_of_sensor_update_policies(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sensor-update/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def delete_a_set_of_sensor_update_policies(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sensor-update/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.delete(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def create_sensor_update_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sensor-update/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def update_sensor_update_policies(self, url, client_id, client_secret, headers="", queries="", body=""):
        params={}
        request_headers={}
        url=f"{url}/policy/entities/sensor-update/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.patch(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def take_action_on_hosts(self, url, client_id, client_secret, action_name, headers="", queries="", body=""):
        params={}
        request_headers={"Content-Type": "application/json","Accept": "application/json"}
        url=f"{url}/devices/entities/devices-actions/v2?action_name={action_name}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.post(url, headers=request_headers, params=params, data=body)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def search_for_hosts(self, url, client_id, client_secret, headers="", queries="", offset="", limit="", sort="", filter=""):
        params={}
        request_headers={}
        url=f"{url}/devices/queries/devices/v1"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        if limit:
            params["limit"] = limit
        if sort:
            params["sort"] = sort
        if filter:
            params["filter"] = filter

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def retrieve_specific_actors_using_their_actor_ids(self, url, client_id, client_secret, ids, headers="", queries="", fields=""):
        params={}
        request_headers={}
        url=f"{url}/intel/entities/actors/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


    def get_pattern_severities_by_id(self, url, client_id, client_secret, ids, headers="", queries=""):
        params={}
        request_headers={}
        url=f"{url}/ioarules/entities/pattern-severities/v1?ids={ids}"
        request_headers=self.setup_headers(headers)
        params=self.setup_params(queries)

        ret = requests.get(url, headers=request_headers, params=params)
        try:
            return ret.json()
        except json.decoder.JSONDecodeError:
            return ret.text


if __name__ == "__main__":

    Crowdstrike_Falcon.run()
