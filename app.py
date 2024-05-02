{
 "cells": [
  {
   "cell_type": "markdown",
   "id": "c60cfb4e-baf0-49a2-b5a0-a72e92399076",
   "metadata": {},
   "source": [
    "# PREDICTION APPLICATION"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 56,
   "id": "9ad59556-a36f-45fb-bccf-bae0bcaa0af0",
   "metadata": {},
   "outputs": [],
   "source": [
    "import streamlit as st"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 57,
   "id": "c6731432-8542-4bb8-b24e-80bd2eb19dc5",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 58,
   "id": "cece2688-05a2-4912-a5ea-5a6351df9455",
   "metadata": {},
   "outputs": [],
   "source": [
    "import subprocess"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 59,
   "id": "681bbf81-c7ae-4f6b-a6ee-2b2e364ed9b8",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 60,
   "id": "5fb788a5-8b0a-47ed-a4b6-7f4cd3b64263",
   "metadata": {},
   "outputs": [],
   "source": [
    "import base64"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 61,
   "id": "cf761666-e6d8-4de8-b856-13f1b095b13c",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pickle\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "81790100-5c2d-4120-9e48-75073e639d58",
   "metadata": {},
   "source": [
    "# Molecular descriptor calculator"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 62,
   "id": "17bb8df4-ebe6-499e-8a39-5ff93ec77bab",
   "metadata": {},
   "outputs": [],
   "source": [
    "def desc_calc():\n",
    "    # Performs the descriptor calculation\n",
    "    bashCommand = \"java -Xms2G -Xmx2G -Djava.awt.headless=true -jar ./PaDEL-Descriptor/PaDEL-Descriptor.jar -removesalt -standardizenitro -fingerprints -descriptortypes ./PaDEL-Descriptor/PubchemFingerprinter.xml -dir ./ -file descriptors_output.csv\"\n",
    "    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)\n",
    "    output, error = process.communicate()\n",
    "    os.remove('molecule.smi')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "cd47418c-f6cc-4ad4-b24d-266829875c63",
   "metadata": {},
   "source": [
    "# File download"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 63,
   "id": "394af741-d7b2-46fc-9f5c-6b66f0016c8a",
   "metadata": {},
   "outputs": [],
   "source": [
    "def filedownload(df):\n",
    "    csv = df.to_csv(index=False)\n",
    "    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions\n",
    "    href = f'<a href=\"data:file/csv;base64,{b64}\" download=\"prediction.csv\">Download Predictions</a>'\n",
    "    return href\n"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "77e29922-26f2-4a9b-9044-dd44c8e36e85",
   "metadata": {},
   "source": [
    "# Model building"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 64,
   "id": "162b3ed5-bfa6-43ee-b5cd-3ca88271af27",
   "metadata": {},
   "outputs": [],
   "source": [
    "def build_model(input_data, load_data):\n",
    "    # Reads in saved regression model\n",
    "    load_model = pickle.load(open('Mtb hsp 60_model.pkl', 'rb'))\n",
    "    # Apply model to make predictions\n",
    "    prediction = load_model.predict(input_data)\n",
    "    st.header('**Prediction output**')\n",
    "    prediction_output = pd.Series(prediction, name='pIC50')\n",
    "    molecule_name = pd.Series(load_data[1], name='molecule_name')\n",
    "    df = pd.concat([molecule_name, prediction_output], axis=1)\n",
    "    st.write(df)\n",
    "    st.markdown(filedownload(df), unsafe_allow_html=True)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "332c7e78-8f95-4a35-88ed-ef44e41de28b",
   "metadata": {},
   "source": [
    "# Sidebar"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 65,
   "id": "698328d6-3b7c-4e02-8394-6427c77571fa",
   "metadata": {},
   "outputs": [],
   "source": [
    "with st.sidebar.header('1. Upload your CSV data'):\n",
    "    uploaded_file = st.sidebar.file_uploader(\"Upload your input file\", type=['txt'])\n",
    "    st.sidebar.markdown(\"\"\"\n",
    "    [Example input file](https://github.com/DavisonChitakatira/data/blob/main/final%20project.csv)\n",
    "    \"\"\")\n",
    "\n",
    "if st.sidebar.button('Predict'):\n",
    "    load_data = None  # Declare load_data variable outside the if statement\n",
    "    if uploaded_file is not None:\n",
    "        load_data = pd.read_table(uploaded_file, sep=' ', header=None)\n",
    "        load_data.to_csv('molecule.smi', sep='\\t', header=False, index=False)\n",
    "\n",
    "    st.header('**Original input data**')\n",
    "    st.write(load_data)\n",
    "\n",
    "    with st.spinner(\"Calculating descriptors...\"):\n",
    "        desc_calc()\n",
    "\n",
    "# load_data is accessible outside the if statement"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "fb2b523a-5403-4954-bb74-905bd23f34f0",
   "metadata": {},
   "source": [
    "# Read in calculated descriptors and display the dataframe"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 66,
   "id": "f8179e15-314f-48ef-a370-bd5275e1d1da",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 85,
   "id": "a0c4ee56-6845-489b-a32e-07c0229d37df",
   "metadata": {},
   "outputs": [],
   "source": [
    " import requests\n",
    "import io\n",
    "\n",
    "url = 'https://github.com/DavisonChitakatira/data/raw/main/descriptors_output%20(1).csv'\n",
    "response = requests.get(url)\n",
    "\n",
    "if response.status_code == 200:\n",
    "    desc = pd.read_csv(io.StringIO(response.content.decode('utf-8')))\n",
    "    st.header('**Calculated molecular descriptors**')\n",
    "    st.write(desc)\n",
    "    st.write(desc.shape)\n",
    "else:\n",
    "    st.error('Failed to fetch the data from the URL.')"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "62875a89-0a08-467f-93b4-c0bd3e5a04f7",
   "metadata": {},
   "source": [
    "# Read descriptor list used in previously built model"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 68,
   "id": "16fc0da3-1b02-459f-a69f-d420906b734e",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 69,
   "id": "5fe0289e-20d4-43d3-b062-ed0e5e240d7b",
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "DeltaGenerator()"
      ]
     },
     "execution_count": 69,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "st.header('**Subset of descriptors from previously built models**')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 70,
   "id": "71d4d7a4-78ce-4716-bdf7-9b5a43bea27d",
   "metadata": {},
   "outputs": [],
   "source": [
    "Xlist = list(pd.read_csv('descriptor_list.csv').columns)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 71,
   "id": "d19e340e-1d70-451a-8318-b55ad8437840",
   "metadata": {},
   "outputs": [],
   "source": [
    "desc_subset = desc[Xlist]\n",
    "st.write(desc_subset)\n",
    "st.write(desc_subset.shape)"
   ]
  },
  {
   "cell_type": "markdown",
   "id": "2ea20452-d6f9-4667-8bbb-12bfccf6a908",
   "metadata": {},
   "source": [
    " # Apply trained model to make prediction on query compounds\n",
    "    "
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 72,
   "id": "9e4b6581-b69d-42c9-a5a5-511a74be4461",
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 73,
   "id": "e4d05c35-b379-47a7-81f5-350ec6fa1471",
   "metadata": {},
   "outputs": [],
   "source": [
    "desc_subset = desc[Xlist]  # Assuming desc_subset is a list of some values\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 81,
   "id": "11c5bf9f-7bb7-47ae-a8b6-a03747d3b28c",
   "metadata": {},
   "outputs": [],
   "source": [
    "load_data = None\n",
    "\n",
    "if len(desc_subset) > 0:\n",
    "    if uploaded_file is not None:\n",
    "        load_data = pd.read_table(uploaded_file, sep=' ', header=None)\n",
    "        load_data.to_csv('molecule.smi', sep='\\t', header=False, index=False)\n",
    "        build_model(desc_subset, load_data)\n",
    "    else:\n",
    "        st.info('Please upload an input file.')\n",
    "else:\n",
    "    st.info('Upload input data in the sidebar to start!')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 82,
   "id": "bb713fd7-9e92-4ef6-b715-4209df92ef52",
   "metadata": {},
   "outputs": [],
   "source": [
    "import os\n",
    "\n",
    "desktop_path = os.path.join(os.path.expanduser(\"~\"), \"Desktop\")\n",
    "streamlit_folder_path = os.path.join(desktop_path, \"streamlit\")\n",
    "\n",
    "# Create the streamlit folder if it doesn't exist\n",
    "if not os.path.exists(streamlit_folder_path):\n",
    "    os.makedirs(streamlit_folder_path)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "id": "7415c75a-8e1c-4372-9507-772c8fba4030",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.19"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
