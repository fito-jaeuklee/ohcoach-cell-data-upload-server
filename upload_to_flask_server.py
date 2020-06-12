import requests
import os

upload_url = 'http://127.0.0.1:5000/fileUpload'
data_dir_path = 'C:/Users/jaeuk/Downloads/data/'


'''
데이터가 저장되는 폴더에서 쓰기가 끝난( line2 를 읽고 있다면 line1의 데이터 6개 셀 모두 데이터가 있다면
총 12개의 데이터) 데이터의 이름을 리턴해주는 함수.

gps/imu 데이터가 없는 cell은 파일이 없기 때문에 yes_data_serial_number를 이용해서
이전 라인의 데이터 이름들을 가지고 온다.
'''


def get_data_name_from_directory(data_save_path, yes_data_serial_number_list):
    output2 = os.listdir(data_save_path)
    data_index_cnt = 0
    will_be_save_file = []
    data_name = []

    for data in output2:
        cell_serial_number = data.split('_')[0]
        data_index_cnt += 1
        for i in range(0, len(yes_data_serial_number_list)):
            print("cell_serial_number = ", cell_serial_number)
            print("input_cell_serial_number = ", yes_data_serial_number_list[i])
            if cell_serial_number == yes_data_serial_number_list[i]:
                print("Find matched serial number data file")
                will_be_save_file.append(data_index_cnt)
            else:
                print("Not matched")

    print(will_be_save_file)

    print("gp/im file targeted by input serial number.")
    print("They will be transmit to flask sever.")
    print("yes_data_serial_num[] = output2[index-1]")
    for index in will_be_save_file:
        print(output2[index - 1])
        data_name.append(output2[index - 1])

    print(data_name)
    return data_name


'''
get_data_name_from_directory 에서 받아온 데이터의 파일명들을 
flask 서버에 post 할 수 있는 타입으로 변경시킨 다음 서버로 보낸다.
'''


def send_data_to_ohcoach_flask_server():
    file_list = []
    data_name_list = get_data_name_from_directory(data_dir_path, ['4', '5', '1', '2', '3', '6'])
    for file in data_name_list:
        one_file = ('file', open(data_dir_path + file, 'rb'))
        file_list.append(one_file)
    print(file_list)

    res = requests.post(url=upload_url, files=file_list)
    print(res.text)


if __name__ == '__main__':
    send_data_to_ohcoach_flask_server()
