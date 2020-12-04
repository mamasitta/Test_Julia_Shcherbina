import csv

# from django.http import HttpResponse
#
#
# def getfile(request):
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="file.csv"'
#     writer = csv.writer(response)
#     writer.writerow(['1001', 'John', 'Domil', 'CA'])
#     writer.writerow(['1002', 'Amit', 'Mukharji', 'LA', '"Testing"'])
#     return response
#
# import csv
# from io import StringIO
# from django.core.files.base import ContentFile
#
# row = ["Name", "Location", "Price"]
#
# csv_buffer = StringIO()
# csv_writer = csv.writer(csv_buffer)
# csv_writer.writerow(row)
#
# csv_file = ContentFile(csv_buffer.getvalue().encode('utf-8'))
#
# bill.bill.save('output.csv', csv_file)
