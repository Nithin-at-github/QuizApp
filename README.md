# QuizApp

## This is an online quiz website where, users can register themselves and participate in quizzes.

This website is hosted at the following link : https://quizapp2022.pythonanywhere.com/

QuizApp is a platform that can host various types of quizzes. Quizzes can have any number of questions, can specify the marks for each questions and questions can 
carry negative marks, if needed. Also we can specify the time limit for quizzes. Users can register themselves to the website by providing the required details like 
username, email, password etc. There will be a captcha verification section on pages like registration, password reset etc as an extra layer of security. Later there 
will be an email verification process to avoid invalid email ids.

### Languages Used : HTML, CSS, JavaScript, Python - Django

Let's take a look at the features of this website.

1. #### Login
   The homepage contains a login section, both users and the administrator can use this section to login to their accounts.
   
   ![home](https://user-images.githubusercontent.com/104214308/213701000-8890f9e3-1baf-48c8-b2bf-415c97eb082b.png)

2. #### Forgot Password
   The homepage also contains a forgot password link, which will redirect you to a page where you can have a password reset link via email using your Username.
   
   ![forgot_pass](https://user-images.githubusercontent.com/104214308/213702059-ea6a9dfe-5d5f-4f61-b847-684225787d3a.png)

3. #### Register
   If you are new to the website you can use the register link in the homepage to go to the registration page. You need to fill all the required fields including captcha to proceed.
   
   ![register](https://user-images.githubusercontent.com/104214308/213702662-e31d3fb4-4186-45a9-a052-130954560898.png)

4. #### Add Quiz
   This section is only available for the administrator. After logging into the admin account there will be an add quiz link to redirect you to the corresponding page.
   
   ![admin_add_quiz](https://user-images.githubusercontent.com/104214308/213703764-de32f0b1-e6db-48dc-bfa2-c561f9d57b0f.png)

5. #### Admin Dashboard
   The admin dashboard will have the list of all available quizzes, and their corresponding links for adding/updating questions, editing and deleting quiz.
   
   ![admin_dash](https://user-images.githubusercontent.com/104214308/213705146-f86baf6d-6412-49b0-bd39-40628c213d65.png)

6. #### Admin view Results
   The administrator can view results of all quizzes on this page. Admin will be notified whenever new results arrive. There is an option to download the result. 
   Admin can also see the submitted answers by checking logs.
   
   ![admin_view_results](https://user-images.githubusercontent.com/104214308/213706536-82a85830-9581-43a6-b3e1-561e29babf73.png)
   After clicking view button the result will show as follows,
   
   ![view_result](https://user-images.githubusercontent.com/104214308/213708797-5e097128-648c-4b98-93f1-48543d5ae441.png)
   The quiz logs will be as follows,
   
   ![quiz_logs1](https://user-images.githubusercontent.com/104214308/213709642-ed3bc2cd-e85d-489d-af07-91bc744d2b56.png)
   ![quiz_logs2](https://user-images.githubusercontent.com/104214308/213709728-f7a001fc-d5b7-4603-a4db-0f4c907bed5b.png)

7. #### View Users
   Administrator can view all registered users including users who did'nt activated their account using email verification in this page. Also admin can remove users
   from here.
   
   ![admin_view_users](https://user-images.githubusercontent.com/104214308/213707602-f5daab60-bd5f-4c26-bcea-880e1bf593c0.png)

8. #### User Dashboard
   The User dashboard will have the list of quizzes that the user can attend. User can attend the quiz by clicking the attempt button.
   
   ![user_dash](https://user-images.githubusercontent.com/104214308/213712886-55ee184f-3600-41de-888e-bb53cb05a5d1.png)
   this will redirect you to the instructions page
   
   ![quiz_instructions](https://user-images.githubusercontent.com/104214308/213713113-7ced63cd-8ad0-49a9-ac04-afe64920be89.png)
   By clicking the start quiz button, user will enter the quiz window 
   
   ![quiz_window](https://user-images.githubusercontent.com/104214308/213713747-076415e7-7325-4066-a78f-d58168db625f.png)

9. #### User Check Results
   This is a common section to check results. Users can get any results by giving the quiz name and candidate id.
   
   ![user_check_results](https://user-images.githubusercontent.com/104214308/213715063-fbfbe70c-f44d-452f-9d47-7531a3e4467b.png)

10. #### Add Feedback
    Users can add feedback about the quizzes and the website through this section.
   
    ![user_add_feedback](https://user-images.githubusercontent.com/104214308/213715496-3673a7ad-6d2b-464b-9716-c00e6bf72355.png)

11. #### Admin View Feedbacks 
   Admin will be notified whenever there is a new feedback. admin can view the feedback and reply in this section.
   
   ![admin_view_feedbacks](https://user-images.githubusercontent.com/104214308/213716734-fbaf452d-1181-4f5d-999c-829d7fd74fd6.png)

12. #### User View Feedbacks
    Users can view feedbacks posted by them in this section. They can also edit them and view replys from admin.
    
    ![user_view_feedback](https://user-images.githubusercontent.com/104214308/213721530-84ea0188-9cbf-490d-baca-243246eee3c4.png)

13. #### User Account Settings
    Users can manage their account in this section.
    
    ![user_settings](https://user-images.githubusercontent.com/104214308/213721965-c9f03a17-0431-4db6-b174-5c398e3ece59.png)

14. #### View Feedbacks
    The latest feedbacks posted by various users is shown in the homepage as visible to everyone. There is a see more button to see all feedbacks as follows. 
    
    ![feedbacks](https://user-images.githubusercontent.com/104214308/213722803-51fdef11-6799-45f7-a800-61d5b8798aa9.png)

15. #### Contact Us
    If there is any queries or any complaints, anyone including registered and non registered users can contact the admin using this section.
    
    ![contact](https://user-images.githubusercontent.com/104214308/213725622-bda872f6-9ace-4e5b-b28e-934fc277c450.png)
