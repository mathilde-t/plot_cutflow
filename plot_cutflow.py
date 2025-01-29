
import matplotlib.pyplot as plt
import mplhep
import pickle
import numpy as np
import sys

def get_hist_values(pickle_file, category):
    file_obj = open(path22, 'rb')
    data = pickle.load(file_obj)
    cuts = [] # = list(data.axes['step']) # or hist.axes['step']
    values = []
    sums = []
    for cut_name in list(cuts): # hist.axes[1]
        cuts.append(f'{cut_name}')
        values.append(data[category,:,f'{cut_name}',:,:].values())
        sums.append(data[category,:,f'{cut_name}',:,:].sum())
    return cuts, values, sums

def create_cutflow_histogram(cuts, data, xlabel="Selections", ylabel="Selection efficiency", title="", log=False, rel=False, save_path=None):
    """
    Create a cutflow histogram using Matplotlib with CMS style and save it to a PDF file.

    Parameters:
    - cuts: List of strings representing the names of the cuts / steps.
    - data: List of integers representing the corresponding event counts for each cut.
    - xlabel: Label for the x-axis (default is "Cuts").
    - ylabel: Label for the y-axis (default is "Events").
    - title: Title of the plot (default is "Cutflow Histogram").
    - save_path: Path to save the PDF file. If None, the plot will be displayed but not saved.

    Returns:
    - fig: Matplotlib figure object.
    - ax: Matplotlib axis object.
    """

    # Set CMS style
    plt.style.use(mplhep.style.CMS)
   
    # Create Matplotlib figure and axis
    fig, ax = plt.subplots()
    if log: plt.yscale('log')

    for i, step in enumerate(cuts):
        n_evt = sums[i]['value']
        ax.step(step, round(n_evt, 2), color='black', where='mid',marker='o', linewidth=1.2, alpha=0.8)#, label=r"Tau_2022C Data-tobeset")
        
        the_txt = f'{n_evt:.4f}' if rel else f'{n_evt:.0f}'
        ax.annotate(the_txt, (step, n_evt), textcoords="offset points", xytext=(0,-20), ha='center', fontsize=10)

    if log:
        if rel: ax.set_ylim((1*10**-6,2*10**0))
        else: 
            pow_nevt = int(np.log10(n_evt[0]))+1.1
            ax.set_ylim((10**(2),10**pow_nevt))

    # Set labels and title
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticklabels(cuts, rotation=45, ha='right')

    # Add legend
    ax.legend()
    ax.grid(True, which='both', axis='y')
    ax.grid(True, which='major', axis='x')
    label_options = {
        "wip": "Work in progress",
        "pre": "Preliminary",
        "pw": "Private work",
        "sim": "Simulation",
        "simwip": "Simulation work in progress",
        "simpre": "Simulation preliminary",
        "simpw": "Simulation private work",
        "od": "OpenData",
        "odwip": "OpenData work in progress",
        "odpw": "OpenData private work",
        "public": "",
    }
    cms_label_kwargs = {
        "ax": ax,
        "llabel": label_options.get("simwip"),
        "fontsize": 22,
        "data": True,
        'rlabel': step
    }
    mplhep.cms.label(**cms_label_kwargs)
    plt.tight_layout()
    
     # Save to PDF if save_path is provided
    if save_path:
        fig.savefig(save_path, bbox_inches='tight')
        print(f"Plot saved to {save_path}")
    else:
        # Show the plot if save_path is not provided
        plt.show()

    return fig, ax




path22 = '/eos/user/m/mwitt/CPinHToTauTauOutput/cf_store/analysis_httcp/cf.CreateCutflowHistograms/run3_2022_preEE_nano_cp_tau_v14/h_ggf_tautau_uncorrelatedDecay_CPodd_Filtered_ProdAndDecay/nominal/calib__main/sel__main__steps_json_met_filter_trigger_dilepton_veto_has_at_least_1_pair_extra_lepton_veto_One_higgs_cand_per_event_has_proper_tau_decay_products_jet_veto_map/Run3_2022PreEE_limited_9jan_kine_v7/cutflow_hist__cf_npvs.pickle'
cat_mutau = 2
cat_incl = 1 # 0 = ?

cuts, values, sums = get_hist_values(path22, cat_mutau)

create_cutflow_histogram(cuts, 
                         data={"2022 preEE": values, "sums": sums},
                         save_path="/eos/user/m/mwitt/CPinHToTauTauOutput/cutflow_histogram_npvs.png",
                         ylabel="N evt",
                         log=True,
                         rel=False)