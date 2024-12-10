import pandas as pd
import matplotlib.pyplot as plt
import os
import csv

def get_main_folder(cell_id):
    currdir=os.getcwd()
    top_dir=os.path.join(currdir,f"data\\{cell_id}")
    print(currdir)
    print(top_dir)
    return top_dir

def load_results(cell_id):
    top_dir=get_main_folder(cell_id)
    pos_file=os.path.join(top_dir,"maxshiftp.csv")
    neg_file=os.path.join(top_dir,"maxshiftp.csv")

    # Initialize an empty dictionary to store results
    summary_datap = {}
    summary_datan = {}
    for folder_name in os.listdir(top_dir):
        # Construct the full path
        folder_path = os.path.join(top_dir, folder_name)

          # Check if it's a directory
        if os.path.isdir(folder_path):
            print(f"Processing folder: {folder_name}")
            results_file=os.path.join(folder_path,"results_summary.csv")

            if os.path.exists(results_file):
                # Load the results summary file
                data = pd.read_csv(results_file)

                # Extract the E value, CFreq, and max_shiftp
                for _, row in data.iterrows():
                    E = row["E"]
                    CFreq = row["CFreq"]
                    max_shiftp = row["max_shiftp"]
                    max_shiftn=row["max_shiftn"]

                    # Initialize row if not present
                    if E not in summary_datap:
                        summary_datap[E] = {}
                        summary_datan[E] = {}

                    # Add the max_shiftp for this CFreq
                    summary_datap[E][CFreq] = max_shiftp
                    summary_datan[E][CFreq] = max_shiftn
            else:
                print(f"Warning: Results file not found in {folder_path}")

    # Convert the dictionary to a DataFrame
    summary_dfp = pd.DataFrame(summary_datap).T
    summary_dfp.index.name = "E"
    output_p=os.path.join(top_dir,"maxshiftp.csv")
    summary_dfp.to_csv(output_p)
    print(f"Summary saved to {output_p}")
    summary_dfn = pd.DataFrame(summary_datan).T
    summary_dfn.index.name = "E"
    output_n=os.path.join(top_dir,"maxshiftn.csv")
    summary_dfn.to_csv(output_n)

    return summary_dfp,summary_dfn,top_dir
        
def plot_results(summary_df,title="Max Shiftp",top_dir=None):
   # Extract E values (index) and carrier frequencies (columns)
    E_values = summary_df.index.tolist()
    CFreq_columns = summary_df.columns.tolist()
    ax,fig=plt.subplots()
    for CFreq in CFreq_columns:
        ax.plot(E_values, summary_df[CFreq], label=f"CFreq {CFreq} Hz")
      # Add labels, title, legend, and grid
    ax.set_xlabel("E (Electric Field Strength)", fontsize=12)
    ax.set_ylabel(f"title", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend(title="Carrier Frequency", fontsize=10)
    ax.grid(True)

    if top_dir:
        out_file=os.path.join(top_dir,f"{title}.png")
        fig.savefig(out_file, dpi=300, bbox_inches='tight')
        print(f"Plot saved to {out_file}")

