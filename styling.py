# Styling for Pyplot


import seaborn as sns


# BASE COLORS

C_PICOM ='#014992'
C_PETROL = '#0A7492'
C_LIGHT = '#CAE5CA'
C_ORAN = '#F6A136'
C_RED = '#CB4A48'
C_TURQ = '#219C9D'
C_SAND = '#E7D15F'
C_GREEN = '#2BC188'
C_YELL = '#EFD655'
C_PURPLE = '#54568F'
C_PALEBLU = '#277996'
C_PALEGRE = '#80A89A'
C_PALEYELL = '#D4CC81'

# COLOR GRAD

GRAD = [
    '#014992', '#254a95', '#394b97', '#484c99',
    '#564c9b', '#634c9c', '#704d9c', '#7b4d9d',
    '#864d9c', '#914e9c', '#9b4e9a', '#a54e99',
    '#ae4f97', '#b75095', '#c05192', '#c8538f',
    '#cf558c', '#d65789', '#dd5a85', '#e35d81',
    '#e8617e', '#ee657a', '#f26976', '#f66e72',
    '#f9746e', '#fc796a', '#ff7f66', '#ff8562',
    '#ff8b5f', '#ff925b', '#ff9858', '#ff9f56',
    '#ffa653', '#ffad51', '#ffb450', '#fcbb4f',
    '#fac150', '#f7c850', '#f3cf52', '#efd655'
    ]


sns.set(font='Arial Narrow',
        rc={
            'axes.axisbelow': False, 'axes.edgecolor': 'lightgrey', 
            'axes.facecolor': 'None', 'axes.grid': False,
            'axes.labelcolor': 'dimgrey', 'axes.spines.right': False,
            'axes.spines.top': False, 'figure.facecolor': 'white',
            'lines.solid_capstyle': 'round', 'patch.edgecolor': 'w',
            'patch.force_edgecolor': True, 'text.color': 'dimgrey',
            'xtick.bottom': True, 'xtick.color': 'lightgrey',
            'xtick.labelcolor': 'dimgrey', 'ytick.labelcolor': 'dimgrey',
            'xtick.direction': 'out', 'xtick.top': False,
            'ytick.color': 'lightgrey', 'ytick.direction': 'out',
            'ytick.left': True, 'ytick.right': False,
            'font.weight': 'light',
            })

sns.set_context("notebook", rc={"font.size":16,
                                "axes.titlesize":20,
                                "axes.labelsize":18})

# Use rcParams to get the styling options