from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType
from home_auth.models import CustomUser
import sys

class Command(BaseCommand):
    help = 'Set up admin permissions and groups for full access'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            help='Username of the admin user to grant permissions to'
        )

    def handle(self, *args, **options):
        username = options.get('username')
        
        # Get or create Admin group with all permissions
        admin_group, created = Group.objects.get_or_create(name='Administrators')
        
        # Get all permissions
        all_permissions = Permission.objects.all()
        
        # Add all permissions to Admin group
        admin_group.permissions.set(all_permissions)
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Created "Administrators" group with all permissions')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Updated "Administrators" group with all permissions')
            )
        
        # If username provided, grant admin status to that user
        if username:
            try:
                user = CustomUser.objects.get(username=username)
                user.is_staff = True
                user.is_superuser = True
                user.is_authorized = True
                user.is_admin = True
                user.save()
                
                # Add user to Admin group
                user.groups.add(admin_group)
                
                self.stdout.write(
                    self.style.SUCCESS(f'✓ User "{username}" promoted to SUPERUSER with full permissions')
                )
            except CustomUser.DoesNotExist:
                self.stdout.write(
                    self.style.ERROR(f'✗ User "{username}" does not exist')
                )
                sys.exit(1)
        else:
            self.stdout.write(
                self.style.WARNING('Note: To promote an existing user, use: python manage.py setup_admin_permissions --username <username>')
            )
        
        self.stdout.write(self.style.SUCCESS('\n✓ Admin permissions setup completed successfully!'))
        self.stdout.write('Access the admin panel at: http://127.0.0.1:8000/admin/')
