import argparse
import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from t8_client.models.spectra import SpectraData


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare spectra")
    parser.add_argument("path", help="Path to the spectrum file")
    args = parser.parse_args()
    computed_path = args.path.replace(".json", "_computed.json")
    
    retrieved_spectrum = SpectraData.parse_obj(json.load(open(args.path)))
    
    computed_file = json.load(open(computed_path))
    computed_freqs = np.array(computed_file["frequencies"], dtype=np.float32)
    computed_amps = np.array(computed_file["amplitudes"], dtype=np.float32)
    
    # Figura para subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

    # Plot del espectro computado
    ax1.plot(computed_freqs, computed_amps,color="orange")
    ax1.set_title("Computed Spectrum")
    
    # Deshabilitar plt.show en SpectraData.plot
    original_show = plt.show 
    plt.show = lambda: None 

    try:
        retrieved_spectrum.plot()
        fig_objeto = plt.gcf()
        ax_objeto = fig_objeto.gca()
        for line in ax_objeto.get_lines():
            ax2.plot(line.get_xdata(), line.get_ydata(), 
                    label=line.get_label(), color=line.get_color(),
                    linestyle=line.get_linestyle())
    
        # Copiamos también el título si lo tiene
        ax2.set_title(ax_objeto.get_title())
        
        # Cerramos la figura extra que creó el objeto para que no moleste
        plt.close(fig_objeto)
        
    finally:
        plt.show = original_show

    plt.tight_layout()
    plt.savefig("data/plots/comparison_spectrum.png")
    print("Imagen guardada como comparison_spectrum.png")

if __name__ == "__main__":
    main()