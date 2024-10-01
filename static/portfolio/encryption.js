const encrypt_options = [
    { method: 'atbash', func: atbashCipher },
    { method: 'caesar', func: caesarCipher },
    { method: 'vigenere', func: vigenereCipher }
];
const alphabet = 'abcdefghijklmnopqrstuvwxyz';

// Caesar Cipher
function caesarCipher(text, shift = 3) {
    return text.split('').map(char => {
        if (/[a-zA-Z]/.test(char)) {
            const base = char === char.toUpperCase() ? 65 : 97;
            return String.fromCharCode((char.charCodeAt(0) - base + shift + 26) % 26 + base);
        } else {
            return char;
        }
    }).join('');
}

// Atbash Cipher
function atbashCipher(text) {
    const reversedAlphabet = alphabet.split('').reverse().join('');
    const translationTable = [...alphabet, ...alphabet.toUpperCase()].reduce((acc, char, i) => {
        acc[char] = reversedAlphabet[i % 26];
        acc[char.toUpperCase()] = reversedAlphabet[i % 26].toUpperCase();
        return acc;
    }, {});
    
    return text.split('').map(char => translationTable[char] || char).join('');
}

// Vigenere Cipher
function vigenereCipher(text, key, encrypt = true) {
    key = key.toUpperCase();
    let keyIndex = 0;

    return text.split('').map(char => {
        if (/[a-zA-Z]/.test(char)) {
            const base = char === char.toUpperCase() ? 65 : 97;
            const shift = (key.charCodeAt(keyIndex % key.length) - 65) * (encrypt ? 1 : -1);
            keyIndex++;
            return String.fromCharCode((char.charCodeAt(0) - base + shift + 26) % 26 + base);
        } else {
            return char;
        }
    }).join('');
}

// Encrypt Username
function encryptUsername(username, encrypt_method) {
    const selectedOption = encrypt_options[encrypt_method];
    let result;
    const shift = Math.floor(Math.random() * 3) + 1;
    const vigenereKey = "IT312";

    if (selectedOption.method === 'caesar') {
        result = selectedOption.func(username, shift); // Pass shift for Caesar cipher
    } else if (selectedOption.method === 'vigenere') {
        result = selectedOption.func(username, vigenereKey); // Pass key for Vigenère cipher
    } else {
        result = selectedOption.func(username); // Atbash cipher doesn't need extra params
    }

    return { result, selectedMethod: selectedOption.method, shift };
}

// Decrypt Username
function decryptUsername(encrypted_username, encrypt_method, shift = 3, vigenereKey = "IT312") {
    if (encrypt_method === 'caesar') {
        return caesarCipher(encrypted_username, -shift); // Reverse shift for decryption
    } else if (encrypt_method === 'atbash') {
        return atbashCipher(encrypted_username); // Same function for encryption and decryption
    } else if (encrypt_method === 'vigenere') {
        return vigenereCipher(encrypted_username, vigenereKey, false); // Decrypt with Vigenère cipher
    } else {
        throw new Error("Unknown encryption method");
    }
}

document.addEventListener("DOMContentLoaded", function () {
    var username = document.getElementById("username").innerHTML;
    var encryption_confirmation = confirm("Do you want to encrypt your username?");

    if (encryption_confirmation && username) {
        var selected_encryption = prompt("Select encryption method:\n1. Caesar Cipher\n2. Atbash Cipher\n3. Vigenère Cipher");

        if (selected_encryption) {
            selected_encryption = parseInt(selected_encryption) - 1; // Adjust selection to 0-indexed array
            
            if (selected_encryption >= 0 && selected_encryption < encrypt_options.length) {
                // Encrypt the username based on the user's choice
                var encrypted_username = encryptUsername(username, selected_encryption);
                alert(`Encrypted Username (${encrypted_username.selectedMethod}): ${encrypted_username.result}`);

                // Ask for decryption
                var decryption_confirmation = confirm("Do you want to decrypt the username?");
                if (decryption_confirmation) {
                    // Decrypt the username
                    var decrypted_username = decryptUsername(
                        encrypted_username.result,
                        encrypt_options[selected_encryption].method,
                        encrypted_username.shift
                    );
                    alert(`Decrypted Username: ${decrypted_username}`);

                    var display_to_url_confirmation = confirm(`Username: ${username} ✔\nEncrypted username: ${encrypted_username.result} ✔\nDecrypted username: ${decrypted_username} ✔\nDo you want to use it as the URL address?`);
                    if (display_to_url_confirmation) {
                        const newUrl = `/${decrypted_username}/${encrypted_username.result}`;
                        window.history.replaceState(null, '', newUrl);
                    }
                }
            } else {
                alert("Invalid selection. Please choose 1, 2, or 3.");
            }
        }
    } else {
        alert("No username provided or encryption declined.");
    }
});
