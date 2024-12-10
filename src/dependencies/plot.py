import plotext as plt

def barplot_fancy(category_names: list,percentages: list,title: str) -> None:
    plt.bar(category_names,percentages)
    plt.title(title)
    plt.show()

def barplot(category_names: list,percentages: list,title: str,width: int = 100) -> None:
    plt.simple_bar(category_names,percentages,width=width,title=title)
    plt.show()