from thorlabs_elliptec import ELLx

stage = ELLx(serial_port="COM5", x=16)

print(f"{stage.model_number} on {stage.port_name},"
        f"serial number {stage.serial_number}, "
        f"status {stage.status.description}")