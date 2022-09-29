import matplotlib.pyplot as plt
import base64
from io import BytesIO


def get_graph():
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    img_png = buffer.getvalue()
    graph = base64.b64encode(img_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph



def get_plot(x,y):
    plt.switch_backend('AGG')

    plt.figure(figsize=(10,5))
    plt.title('Damages')
    plt.bar(x,y)
    plt.xticks(rotation=45)
    plt.xlabel('Item')
    plt.ylabel('Quantity')
    plt.tight_layout()
    graph = get_graph()    
    return graph