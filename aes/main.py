from algorithms.aes.key_schedule import KeySchedule


if __name__ == "__main__":
    key_schedule = KeySchedule()
    key_schedule.expand(b"segurancadainformacao")