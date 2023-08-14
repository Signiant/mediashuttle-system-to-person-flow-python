from flask import Flask
from system_to_person.api_data_handler import create_transfer_link, WorkflowType

app = Flask(__name__)


@app.route('/api/fileAcquisition', methods=['GET'])
def file_acquisition():
    data = create_transfer_link(WorkflowType.FILE_ACQUISITION)
    return data


@app.route('/api/fileDistribution', methods=['GET'])
def file_distribution():
    data = create_transfer_link(WorkflowType.FILE_DISTRIBUTION)
    return data