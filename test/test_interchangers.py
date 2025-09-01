from src.core.interchangers import InterChanger

def test_interchangers() -> None:
    admin =     InterChanger(
        [
            {"letter_a": "A", "letter_b": "E"},
        ]
    )

    input_text = "INTERCAMBIAR LAS LETRAS A Y E"
    output_text = "INTARCEMBIER LES LATRES E Y A"

    result: str = "".join([admin.exchange_letter(letter) for letter in input_text])

    assert result == output_text