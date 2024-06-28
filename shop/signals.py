# from django.db.models.signals import post_save,pre_save
# from django.dispatch import receiver
# from django.core.mail import EmailMultiAlternatives
# from django.template.loader import render_to_string
# from .models import Branch

# @receiver(post_save, sender=Branch)
# def send_branch_creation_email(sender, instance, created, **kwargs):
#     if created:
#         user = instance.shop.user
#         branch_name = instance.name
#         shop_name = instance.shop.name
#         username = instance.user.username
#         password = instance.user.password  # Assuming you store the password securely

#         email_subject = "New Branch Created"
#         email_body = render_to_string('branch.html', {
#             'user': user,
#             'username': username,
#             'password': password,
#             'branch_name': branch_name,
#             'shop_name': shop_name
#         })

#         try:
#             email = EmailMultiAlternatives(email_subject, '', to=[user.email])
#             email.attach_alternative(email_body, "text/html")
#             email.send()
#         except Exception as e:
#             print(f"Failed to send email: {str(e)}")


# @receiver(pre_save, sender=Branch)
# def send_branch_creation_email(sender, instance, **kwargs):
#     if instance._state.adding:  # Checking if the instance is being added (created)
#         user = instance.shop.user
#         branch_name = instance.name
#         shop_name = instance.shop.name
#         username = instance.user.username
#         password = instance.user.password  # Assuming you store the password securely

#         email_subject = "New Branch Creation In Progress"
#         email_body = render_to_string('branch.html', {
#             'user': user,
#             'username': username,
#             'password': password,
#             'branch_name': branch_name,
#             'shop_name': shop_name
#         })

#         try:
#             email = EmailMultiAlternatives(email_subject, '', to=[user.email])
#             email.attach_alternative(email_body, "text/html")
#             email.send()
#         except Exception as e:
#             print(f"Failed to send email: {str(e)}")