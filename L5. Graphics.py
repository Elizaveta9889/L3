from modules import files_work_data_frame as fw_df
from modules import graphics_model as gr
from modules import learning_model as lm
from modules import files_work_data_frame as w_df


df = fw_df.read_files_to_df("L3. ProgrammerGroups")
df = df.fillna(0)
sings = [['1с: розница', '1c: бухгалтерия'], ["github", "работа в команде"], ["html", "css"], ["frontend", "web"], ['c++', 'qt']]
signs_df = gr.signs_df(df, sings)
gr.save_corr_matrix(df, "L5. Graphics/correlation.html")
gr.save_line(signs_df, "L5. Graphics/line.html")
gr.save_bar(signs_df, "L5. Graphics/bar.html")
gr.save_scatter_matrix(signs_df, "L5. Graphics/scatter_matrix.html")
gr.save_word_cloud(df, "L5. Graphics/word_cloud.png")
gr.print_outbursts(df)
gr.save_outbursts_diagram(df, "L5. Graphics/outbursts_diagram.html")
df = gr.change_outbursts(df, "min_salary")
df = gr.change_outbursts(df, "max_salary")
df = gr.delete_outbursts(df, "min_salary")
df = gr.delete_outbursts(df, "max_salary")
gr.save_outbursts_diagram(df, "L5. Graphics/without_outbursts_diagram.html")
w_df.save_data_frame(df, "Vacancies_without_outbursts")