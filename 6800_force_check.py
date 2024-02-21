import streamlit as st
import pandas as pd
from bokeh.plotting import figure
import yaml
from bokeh.models import Range1d, LinearAxis
import zipfile
import matplotlib



#So it is easier to look at the graph(without big vibrations in the lines)
def smoothing_data(array):
    # smoothing data with exponential moving average
    array = array.ewm(span=100).mean()  # best solution

    return array 

def design():
    
    st.title('Current and Position Visualization')


    


    upload_data = st.file_uploader(label = "force check upload", type=None, accept_multiple_files=False)
    # with open('filename.txt', 'w') as name_file:
    #     x = "\n".join(upload_data)
    #     name_file.write(x)


    if not upload_data:
        st.write('Please upload force check data')
    else:
        select = st.selectbox("Select the Pipetor", ("all","1", "2", "3", "4"))
        # global data_temp #must be filled with the data of the enzipped files
        #st.write(upload_data)
        # name of the uploaded zip file for the table name in the database
        with open('zipname.txt', 'w') as zipname:
            zipname.write(upload_data.name)
        
        all_data = []
        name_list = []
        file_name_list = ["A01", "C01", "E01", "G01", "B01", "D01", "F01", "H01", "A03", "C03", "E03", "G03", "B03", "D03", "F03", "H03", "A05", "C05", "E05", "G05", "B05", "D05", "F05", "H05", "A07", "C07", "E07", "G07", "B07", "D07", "F07",
                         "H07", "A09", "C09", "E09", "G09", "B09", "D09", "F09", "H09", "A11", "C11", "E11", "G11", "B11", "D11", "F11", "H11"]
        list_of_color = list(matplotlib.colors.cnames.values())

    #put the data of the uploaded files in a list
        syslog_index_skip = 0
        with zipfile.ZipFile(upload_data, 'r') as zipfiles:
            for index, name in enumerate(zipfiles.namelist()):
                if 'syslog' not in name:
                    if index >= 48:
                        file_name = f'Plate 2 {file_name_list[index-(48+syslog_index_skip)]}'
                    else:
                        file_name = f'Plate 1 {file_name_list[index-syslog_index_skip]}'
                    # TODO: Create name for files and pass them to the all_data.append() instead of the name variable
                    with zipfiles.open(name, 'r') as file:
                        data_temp = data_handler(file)
                        all_data.append([file_name, list_of_color[index], data_temp])
                else:
                    syslog_index_skip = 1

        #st.write(all_data)
        #pipetor auswahl funktion
        if select != 'all':
            start_index = int(select) - 1
            end_index = 92 + int(select)

            pipettor_file_index_list = list(range(start_index, end_index, 4))

            pipettor_file_list = []
            for index in pipettor_file_index_list:
                pipettor_file_list.append(all_data[index])
                name_list.append(all_data[index][0])

            


            st.write(f"{select} selected")

        else:
            pipettor_file_list = all_data
            for file in all_data:
                name_list.append(file[0])
            



        #for the user to decide what graph they want
        currentcheckbox= st.radio(label="Select your graph", options=["Ampere", "Position", "Both Position and Current(Ampere)"])
        #filter for a specific file
        file_select = st.multiselect("Filter for a specific file", options=name_list, default=None)

        filtered_data = []

        #file filter function
        if file_select:
            for f in file_select:
                file_data = next(filter(lambda x: x[0] == f, all_data))
                filtered_data.append(file_data)
            pipettor_file_list = filtered_data
            

        # calculate how many rows are in 3.5 sec (To get x axis)
        rows = int(3.5 * 2500)

        
        time_list =[]
        time = list(x / 2500 for x in range(0, rows))
        actualCurrent_data = []
        effectivePosition_data = []
        actualCurrent_items = []
        color_list = []
        
        
        col1, col2= st.columns([5, 1.5])

        with col1:


            if currentcheckbox=='Ampere':
                #Graph for current(Ampere)
                
                # st.write(all_data)
                for data_set in pipettor_file_list:
                    time_list.append(time)
                    color_list.append(data_set[1])
                    actualCurrent_data.append(data_set[2]['ActualCurrent_Smooth[A]']) 
                    actualCurrent_items.append([data_set[0], data_set[2]['ActualCurrent_Smooth[A]']])


                p = figure(
                title="Graph for Current(Ampere)",
                x_axis_label='Time[s]',
                y_axis_label='ActualCurrent[A]')
                
                p.multi_line(time_list, actualCurrent_data, line_width=2, line_color = color_list)
                
                # legend = Legend(items = actualCurrent_items , location="center")
                # p.add_layout(legend, 'right')

                st.bokeh_chart(p, use_container_width=True) 

            elif currentcheckbox=='Position':
                #Graph for positions
                #st.write(data_temp)
                for data_set in pipettor_file_list:
                    time_list.append(time)
                    color_list.append(data_set[1])
                    effectivePosition_data.append(data_set[2]["EffectivePosition[m]"])
                    actualCurrent_items.append([data_set[0], data_set[2]['ActualCurrent_Smooth[A]']])

                p = figure(
                title="Graph for positions",
                x_axis_label='Time[s]',
                y_axis_label="EffectivePosition[m]")

                p.multi_line(time_list, effectivePosition_data, line_width=2, line_color = color_list)
                p.y_range.flipped = True

                st.bokeh_chart(p, use_container_width=True)

            elif currentcheckbox=='Both Position and Current(Ampere)':
                #Graph where position and Ampere are both displayed

                for data_set in pipettor_file_list:
                    time_list.append(time)
                    color_list.append(data_set[1])
                    actualCurrent_data.append(data_set[2]['ActualCurrent_Smooth[A]']) 
                    effectivePosition_data.append(data_set[2]["EffectivePosition[m]"])
                    actualCurrent_items.append([data_set[0], data_set[2]['ActualCurrent_Smooth[A]']])

                p = figure(
                title="Graph for Position and Ampere",
                x_axis_label='Time[s]')

                #add a y axis
                p.yaxis.axis_label = "EffectivePosition[m]"
                p.y_range = Range1d(start=-0.08, end=-0.11)

                #add a second y axis
                p.extra_y_ranges = {"ActualCurrent_Smooth[A]": Range1d(start=-0.2, end=0.8)}
                p.add_layout(LinearAxis(y_range_name="ActualCurrent_Smooth[A]"), 'right')
            

                p.multi_line(time_list, actualCurrent_data, line_width=2, y_range_name="ActualCurrent_Smooth[A]", line_color = color_list)
                p.multi_line(time_list, effectivePosition_data, line_width=2, line_color = color_list)
                

                st.bokeh_chart(p, use_container_width=True)
        with col2:
           
           with st.expander("See legend"):
                #file legend with colours  
                for file in pipettor_file_list:
                    st.write(f'{file[0]} - <span style="color:{file[1]};">&#9632;</span>', unsafe_allow_html=True)

        
        #put all the data from the uploaded file in a yaml file 
        with open('data.yml', 'w') as yml_file:
            yaml.dump(str(data_set), yml_file)
        
            

def data_handler(upload_data):
    header_DF = ["DesiredCurrent[A]", "ActualCurrent[A]",
                        "PositionError[tbd]", "DesiredPosition[tbd]", "DesiredVelocity[tbd/s]", "N/A", "N/A2"]
    # we don't need the first 4 lines of the csv
    data = pd.read_csv(upload_data, delimiter=',', skiprows=[
                            0, 1, 2, 3], names=header_DF)
    
    data_df = data.drop(columns=['N/A', 'N/A2'], axis=1)
    data_df["EffectivePosition[m]"] = data_df["DesiredPosition[tbd]"] - \
    data_df["PositionError[tbd]"]
    data_df["EffectivePosition_Smooth[m]"] = data_df["EffectivePosition[m]"]

    # multiply with 100 to get cm (everything is normaly in meters)
    data_df["EffectivePosition_Smooth[cm]"] = data_df["EffectivePosition_Smooth[m]"] * 100

    data_df["ActualCurrent_Smooth[A]"] = smoothing_data(
        data_df["ActualCurrent[A]"])

    # get all rows where EffectivePosition[m] higher than -0.1
    data_df = data_df[data_df['EffectivePosition[m]'] >= -0.105]

    rows = int(3.5 * 2500)

    # get all rows till 3.5 sec
    return data_df.head(rows)
         

def main():
    design()

if __name__ == '__main__':
    main()


