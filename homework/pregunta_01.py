# pylint: disable=import-outside-toplevel
# pylint: disable=line-too-long
# flake8: noqa
"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""


def pregunta_01():
    """
    La información requerida para este laboratio esta almacenada en el
    archivo "files/input.zip" ubicado en la carpeta raíz.
    Descomprima este archivo.

    Como resultado se creara la carpeta "input" en la raiz del
    repositorio, la cual contiene la siguiente estructura de archivos:


    ```
    train/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    test/
        negative/
            0000.txt
            0001.txt
            ...
        positive/
            0000.txt
            0001.txt
            ...
        neutral/
            0000.txt
            0001.txt
            ...
    ```

    A partir de esta informacion escriba el código que permita generar
    dos archivos llamados "train_dataset.csv" y "test_dataset.csv". Estos
    archivos deben estar ubicados en la carpeta "output" ubicada en la raiz
    del repositorio.

    Estos archivos deben tener la siguiente estructura:

    * phrase: Texto de la frase. hay una frase por cada archivo de texto.
    * sentiment: Sentimiento de la frase. Puede ser "positive", "negative"
      o "neutral". Este corresponde al nombre del directorio donde se
      encuentra ubicado el archivo.

    Cada archivo tendria una estructura similar a la siguiente:

    ```
    |    | phrase                                                                                                                                                                 | target   |
    |---:|:-----------------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------|
    |  0 | Cardona slowed her vehicle , turned around and returned to the intersection , where she called 911                                                                     | neutral  |
    |  1 | Market data and analytics are derived from primary and secondary research                                                                                              | neutral  |
    |  2 | Exel is headquartered in Mantyharju in Finland                                                                                                                         | neutral  |
    |  3 | Both operating profit and net sales for the three-month period increased , respectively from EUR16 .0 m and EUR139m , as compared to the corresponding quarter in 2006 | positive |
    |  4 | Tampere Science Parks is a Finnish company that owns , leases and builds office properties and it specialises in facilities for technology-oriented businesses         | neutral  |
    ```


    """
    from pathlib import Path
    import re
    import pandas as pd


    repo_root = Path(__file__).resolve().parent.parent
    files_dir = repo_root / "files"
    output_dir = files_dir / "output"

    def encontrar_base_train_test() -> Path:
        candidatos = [
            repo_root / "input",       
            files_dir / "input",
            files_dir / "input" / "input",
        ]
        for base in candidatos:
            if (base / "train").exists() and (base / "test").exists():
                return base

        for p in files_dir.rglob("train"):
            base = p.parent
            if (base / "test").exists():
                return base
        raise FileNotFoundError("No se encontró una carpeta con 'train' y 'test' dentro de 'files/'.")

    base_dir = encontrar_base_train_test()

    def construir_dataset(split: str) -> pd.DataFrame:
        registros = []
        for sentimiento in ("negative", "positive", "neutral"):
            carpeta = base_dir / split / sentimiento
            if not carpeta.exists():
                continue
            for txt in sorted(carpeta.glob("*.txt")):
                texto = txt.read_text(encoding="utf-8", errors="ignore")
                texto = re.sub(r"\s+", " ", texto).strip()
                registros.append({"phrase": texto, "target": sentimiento})
        return pd.DataFrame(registros, columns=["phrase", "target"])

    train_df = construir_dataset("train")
    test_df  = construir_dataset("test")


    output_dir.mkdir(parents=True, exist_ok=True)


    train_df.to_csv(output_dir / "train_dataset.csv", index=False, encoding="utf-8")
    test_df.to_csv(output_dir / "test_dataset.csv", index=False, encoding="utf-8")


    return