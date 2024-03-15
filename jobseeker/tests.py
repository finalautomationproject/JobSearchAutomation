# from django.test import TestCase

# # Create your tests here.
# userinfo.html

# {% extends 'jobseeker/base.html' %}
# {% block title %} Enter Details {% endblock %}

# {% block content %}
# <!-- Button to open the pop-up window -->
# <button onclick="openPopup()">Enter Your Details</button>

# <!-- Pop-up window -->
# <div id="popup" class="popup">
#   <div class="container d-flex justify-content-center align-items-center">
#     <div class="card p-4 popup-content">
#       <h1 class="text-center mb-4">Enter Your Details</h1>
#       <form id="multiStepForm" method="post" enctype="multipart/form-data" class="mt-4">
#         {% csrf_token %}
#         <div id="step1" class="form-step">
#           <!-- Display form fields for step 1 -->
#           <div class="form-group">
#             <label for="id_email">Email</label>
#             <input type="email" id="id_email" name="email" required>
#           </div>
#           <div class="form-group">
#             <label for="id_avatar">Avatar</label>
#             <input type="file" id="id_avatar" name="avatar">
#           </div>
#           <div class="form-group">
#             <label for="id_linkedin_password">LinkedIn Password</label>
#             <input type="password" id="id_linkedin_password" name="linkedin_password" required>
#           </div>
#           <div class="form-group">
#             <label for="id_indeed_password">Indeed Password</label>
#             <input type="password" id="id_indeed_password" name="indeed_password" required>
#           </div>
#           <button type="button" onclick="nextStep()">Next</button>
#         </div>
#         <div id="step2" class="form-step" style="display: none;">
#           <!-- Display form fields for step 2 -->
#           <div class="form-group">
#             <label for="id_keywords">Keywords</label>
#             <input type="text" id="id_keywords" name="keywords">
#           </div>
#           <div class="form-group">
#             <label for="id_location">Location</label>
#             <input type="text" id="id_location" name="location">
#           </div>
#           <div class="form-group">
#             <label for="id_resume">Resume</label>
#             <input type="file" id="id_resume" name="resume">
#           </div>
#           <button type="button" onclick="submitForm()">Submit</button>
#           <button type="button" onclick="prevStep()">Previous</button>
#         </div>
#       </form>
#     </div>
#   </div>
# </div>

# <!-- JavaScript to handle multi-step form -->
# <script>
#   // Function to open the pop-up window
#   function openPopup() {
#     document.getElementById('popup').style.display = 'block';
#   }

#   // Function to move to the next step of the form
#   function nextStep() {
#     document.getElementById('step1').style.display = 'none';
#     document.getElementById('step2').style.display = 'block';
#   }

#   // Function to move to the previous step of the form
#   function prevStep() {
#     document.getElementById('step2').style.display = 'none';
#     document.getElementById('step1').style.display = 'block';
#   }

#   // Function to submit the form
#   function submitForm() {
#     document.getElementById('multiStepForm').submit();
#   }
# </script>
# {% endblock %}
