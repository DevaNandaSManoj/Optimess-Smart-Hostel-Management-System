import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand

from accounts.models import Student
from food.models import StudentDailyRecord


class Command(BaseCommand):
    help = (
        "Seed/overwrite StudentDailyRecord for ALL students from April 6, 2026 "
        "to today. present=True, random breakfast/lunch/dinner, marked_by='student'."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--force",
            action="store_true",
            help="Overwrite existing records (default: skip existing).",
        )

    def handle(self, *args, **options):
        force = options["force"]
        start_date = date(2026, 4, 6)
        end_date = date.today()

        students = list(Student.objects.select_related("user").all())
        if not students:
            self.stdout.write(self.style.WARNING("No students found."))
            return

        self.stdout.write(
            f"{'Overwriting' if force else 'Seeding'} records for "
            f"{len(students)} student(s) from {start_date} to {end_date} …"
        )

        created_count = 0
        updated_count = 0
        skipped_count = 0

        current = start_date
        while current <= end_date:
            for student in students:
                b = random.choice([True, False])
                l = random.choice([True, False])
                d = random.choice([True, False])

                if force:
                    obj, created = StudentDailyRecord.objects.update_or_create(
                        student=student,
                        date=current,
                        defaults={
                            "present": True,
                            "breakfast": b,
                            "lunch": l,
                            "dinner": d,
                            "marked_by": "student",
                        },
                    )
                    if created:
                        created_count += 1
                    else:
                        updated_count += 1
                else:
                    obj, created = StudentDailyRecord.objects.get_or_create(
                        student=student,
                        date=current,
                        defaults={
                            "present": True,
                            "breakfast": b,
                            "lunch": l,
                            "dinner": d,
                            "marked_by": "student",
                        },
                    )
                    if created:                        created_count += 1
                    else:
                        skipped_count += 1

            current += timedelta(days=1)

        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Created: {created_count}, "
                f"Updated: {updated_count}, "
                f"Skipped: {skipped_count}"
            )
        )
