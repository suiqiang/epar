from epar import app

import os
# We'll render HTML templates and access data sent by POST
# using the request object from flask. Redirect and url_for
# will be used to redirect the user once the upload is done
# and send_from_directory will help us to send/show on the
# browser the file that the user just uploaded

from flask import render_template, request, send_from_directory


from werkzeug.utils import secure_filename


# This is the path to the upload directory

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = set(['txt', ''])

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

# # This route will show a form to perform an AJAX request
# # jQuery is loaded to execute the request and update the
# # value of the operation
# @app.route('/')
# def index():
#     return render_template('index.html')


# Route that will process the file upload
@app.route('/upload_plain', methods=['POST'])
def upload_plain():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['PRJDIR'], 'plain', filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    return render_template('upload.html', filenames=filenames, dirname='plain')


# @app.route('/upload_plain', methods=['POST'])
# def upload_plain():
#     # Get the name of the uploaded files
#     uploaded_files = request.files.getlist['file[]']
#     filenames = []
#     for file in uploaded_files:
#         # Check if the file is one of the allowed types/extensions
#         if file and allowed_file(file.filename):
#             # Make the filename safe, remove unsupported chars
#             filename = secure_filename(file.filename)
#             # Move the file form the temporal folder to the upload
#             # folder we setup
#             file.save(os.path.join(app.config['PRJDIR'], 'plain', filename))
#             # Save the filename into a list, we'll use it later
#             filenames.append(filename)
#             # Redirect the user to the uploaded_file route, which
#             # will basicaly show on the browser the uploaded file
#     # Load an html page with a link to each uploaded file
#     return jsonify(filenames)



@app.route('/upload_power', methods=['POST'])
def upload_power():
    # Get the name of the uploaded files
    uploaded_files = request.files.getlist("file[]")
    filenames = []
    for file in uploaded_files:
        # Check if the file is one of the allowed types/extensions
        if file and allowed_file(file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(file.filename)
            # Move the file form the temporal folder to the upload
            # folder we setup
            file.save(os.path.join(app.config['PRJDIR'], 'power', filename))
            # Save the filename into a list, we'll use it later
            filenames.append(filename)
            # Redirect the user to the uploaded_file route, which
            # will basicaly show on the browser the uploaded file
    # Load an html page with a link to each uploaded file
    return render_template('upload.html', filenames=filenames, dirname='power')



# This route is expecting a parameter containing the name
# of a file. Then it will locate that file on the upload
# directory and show it on the browser, so if the user uploads
# an image, that image is going to be show after the upload
# http://www.sharejs.com

@app.route('/uploads/<path:dirname>/<filename>')
def uploaded_file(dirname, filename):
    return send_from_directory(os.path.join(
        os.getcwd(),
        app.config['PRJDIR'],
        dirname),
                               filename)

