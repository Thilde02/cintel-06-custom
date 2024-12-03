import plotly.express as px
from shiny.express import input, ui
from shiny import render
from palmerpenguins import load_penguins
from shinywidgets import output_widget, render_widget, render_plotly
import seaborn as sns
import palmerpenguins
from shiny import reactive

penguins_df = palmerpenguins.load_penguins()

with ui.layout_columns():
    with ui.card():
        " Penguin Data Table "
        @render.data_frame
        def penguinstable_df():
            return render.DataTable(filtered_data(), filters=False,selection_mode='row')
        

    with ui.card():
        "Penguins Data Grid"
        @render.data_frame
        def penguinsgrid_df():
            return render.DataGrid(filtered_data(), filters=False, selection_mode="row")


with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize("selected_attribute",
                       "Penguin Metric",
                       ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

    ui.input_numeric(
        "plotly_bin_count",
        "Plotly Number of Bins",
        20
    )

    ui.input_slider(
        "seaborn_bin_count",
        "Seaborn Number of Bins",
        1,20,10
    )

    ui.input_checkbox_group(
        "selected_species_list",
        "Species",
        ["Adelie","Gentoo","Chinstrap"],
        selected=["Adelie","Gentoo","Chinstrap"],
        inline=False
    )

    ui.hr()

    ui.a(
        "GitHub",
        href= "https://github.com/Thilde02/cintel-02-data.git",
        target="_blank"
    )

ui.page_opts(title="Penguin Data", fillable=True)
with ui.layout_columns():

    @render_plotly
    def plot1():

        fig = px.histogram(
            penguins_df,
            x="bill_length_mm",
            title="Penguins Bill Length Histogram",
            color_discrete_sequence=["purple"],
        )
        fig.update_traces(marker_line_color="yellow", marker_line_width=2)
        return fig

    @render_plotly
   
    def plot2():
        selected_attribute = input.selected_attribute()
        bin_count = input.plotly_bin_count()
        
        fig = px.histogram(
            filtered_data(),
            x=selected_attribute,
            nbins=bin_count,
            title=f"Penguins {selected_attribute} Histogram",
            color_discrete_sequence=["black"], 
        )
        fig.update_traces(marker_line_color="red", marker_line_width=2)
        return fig

with ui.card(full_screen=True):
