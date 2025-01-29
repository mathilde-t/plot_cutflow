# plot_cutflow

A modification of the plot_cutflow function used in the CPHToTauTau analysis framework.

### Idea
1. take the .pickle file which holds the cutflow histogram content
2. using hep, plt, np : plot the cutflow histogram with number of events per cut

plot logic : NOT sequential but : selection a + selection b + selection c + ...
