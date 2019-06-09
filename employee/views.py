from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from employee.models import Employee
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q


class EmployeeChunk(APIView):
    """Get all the brands which is followed by users"""

    def get(self, request, format=None):
        row_count = 1
        response = []
        row_5th_6th = 0
        row_7th_8th = 0
        score_wise_sorted = 0
        # Call query_1 function
        employee_queryset = self.query_1()
        # Call query_2 function
        emp_obj = self.query_2()

        # Pointing index to last
        row_7th_8th = len(emp_obj) - 1
        # Iterate data on employee_queryset and emp_obj
        while (
            score_wise_sorted < len(employee_queryset)
            or emp_obj[row_5th_6th].department == "Waltzz"
            or emp_obj[row_7th_8th].department != "Waltzz"
        ):
            # Append 'Waltzz department data and latest 14 days data in every 5th to 8th index.
            if row_count % 5 == 0:
                # Check if department is Waltzz and append in o/p response.
                if emp_obj[row_5th_6th].department == "Waltzz":
                    # Call prepare_data function to append
                    self.prepare_data(response, emp_obj, row_5th_6th)
                    row_5th_6th += 1
                # Check if department is Waltzz and append in o/p response.
                if emp_obj[row_5th_6th].department == "Waltzz":
                    # Call prepare_data function to append
                    self.prepare_data(response, emp_obj, row_5th_6th)
                    row_5th_6th += 1
                # Check if department is not Waltzz and append in o/p response.
                if emp_obj[row_7th_8th].department != "Waltzz":
                    # Call prepare_data function to append
                    self.prepare_data(response, emp_obj, row_7th_8th)
                    row_7th_8th -= 1
                # Check if department is not Waltzz and append in o/p response.
                if emp_obj[row_7th_8th].department != "Waltzz":
                    # Call prepare_data function to append
                    self.prepare_data(response, emp_obj, row_7th_8th)
                    row_7th_8th -= 1
            # Else insert sorted data based on score.
            elif score_wise_sorted < len(employee_queryset):
                # Append data in o/p response.
                response.append(employee_queryset[score_wise_sorted])
                score_wise_sorted += 1
            row_count += 1
        # Check string query parameter exist.
        if "chunk" in request.GET:
            # Get chunk_id from string query parameter.
            chunk_id = int(request.GET["chunk"])
            # Call function to append cluster chunk data into response.
            cluster_response = self.employee_cluster(response, chunk_id)
            # Return response to client.
            return Response({"employees": cluster_response}, status=status.HTTP_200_OK)
        # Return response to client.
        return Response({"employees": response}, status=status.HTTP_200_OK)

    def query_1(self):
        # Query data from Employee modal in sorted order based on score and
        # daprtment not equal to Waltzz and data not created within 14 days.
        return (
            Employee.objects.all()
            .order_by("-score")
            .exclude(
                Q(department="Waltzz")
                | Q(date_created__gt=datetime.now() + timedelta(days=-14))
            )
            .values()
        )

    def query_2(self):
        # Query data which holds department 'Waltzz' and created user within 14 days.
        # output result would be all data of waltzz department first and then date wise.
        return Employee.objects.raw(
            "select * from employee_employee where department = 'Waltzz' union all select *\
             from employee_employee where date_created >= current_date-14 and department != 'Waltzz'"
        )

    def employee_cluster(self, response, chunk_id):
        # Make cluster of 20 objects.
        cluster_response = []
        start_index = 0
        end_index = 0
        # If chunk_id is 1 then result belongs between 0 to 20.
        if chunk_id == 1:
            start_index = 0
            end_index = 20
        # else should belong to chunk_id * 2 to chunk_id * 2 + 20.
        else:
            start_index = (chunk_id * 10) + 1
            end_index = (start_index + 20) - 1
        # Iterate to cluster 20 object.
        while start_index <= end_index and start_index < len(response):
            cluster_response.append(response[start_index])
            start_index += 1
        # Return result to called function.
        return cluster_response

    def prepare_data(self, response_data, queryset, index):
        # Convert object to json serilizable.
        response_data.append(
            {
                "employee_code": queryset[index].employee_code,
                "department": queryset[index].department,
                "score": queryset[index].score,
                "date_created": queryset[index].date_created,
            }
        )
