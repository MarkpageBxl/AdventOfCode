def disassemble_combo(code: int) -> str:
    if 0 <= code <= 3:
        return f"0x{code}"
    if code == 4:
        return "A"
    if code == 5:
        return "B"
    if code == 6:
        return "C"
    assert False


def disassemble_instr(opcode, operand) -> str:
    combo = disassemble_combo(operand)
    if opcode == 0:  # adv
        return f"adv {combo}"
    elif opcode == 1:  # bxl
        return f"bxl 0x{operand}"
    elif opcode == 2:  # bst
        return f"bst {combo}"
    elif opcode == 3:  # jnz
        return f"jnz {operand}"
    elif opcode == 4:  # bxc
        return f"bxc"
    elif opcode == 5:  # out
        return f"out {combo}"
    elif opcode == 6:  # bdv
        return f"bdv {combo}"
    elif opcode == 7:  # cdv
        return f"cdv {combo}"
    else:
        assert False


def disassemble(program: list[tuple[int, int]]):
    output_buffer = []
    for opcode, operand in program:
        output_buffer.append(disassemble_instr(opcode, operand))
    return "\n".join(output_buffer)
