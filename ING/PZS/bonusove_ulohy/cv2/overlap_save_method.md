
# 📚 Overlap-Save Method for Fast Convolution

The **Overlap-Save Method** is a widely used algorithm for fast linear convolution, especially with long input signals. It leverages the efficiency of the **Fast Fourier Transform (FFT)** and is commonly used in digital signal processing.

---

## 🔧 Overview

Given:
- Input signal: \( x[n] \) of length \( N \)
- Impulse response: \( h[n] \) of length \( M \)
- Block size: \( B \geq M \), often chosen as a power of 2

---

## ⚙️ Key Steps

### 1. **Block Size and Overlap**
```python
L = block_size - M + 1
```
- \( L \): Number of **new samples per block**
- \( M - 1 \): Number of **overlapped samples** from the previous block

---

### 2. **Preprocessing**
```python
h_fft = np.fft.fft(h, block_size)
x_padded = np.concatenate([np.zeros(M-1), x])
```
- **Zero-pad** the filter `h` to length `block_size`
- **Pad** the input `x` at the start with \( M - 1 \) zeros

---

### 3. **Block Processing**
Loop through the signal in chunks of `L`:
```python
for i in range(0, len(x), L):
    x_block = x_padded[i:i + block_size]
    if len(x_block) < block_size:
        x_block = np.concatenate([x_block, np.zeros(block_size - len(x_block))])
```
- Extract a block of size `block_size` (with overlap)
- Pad the block if it's shorter than expected

---

### 4. **FFT Convolution**
```python
X = np.fft.fft(x_block)
Y = np.fft.ifft(X * h_fft).real
```
- Compute the FFT of the current block
- Multiply in frequency domain
- Use inverse FFT to return to time domain

---

### 5. **Discard Corrupted Samples**
```python
y.extend(Y[M-1:])
```
- Discard the first \( M - 1 \) samples (they are invalid due to circular convolution)
- Save only the valid output

---

### 6. **Return Final Output**
```python
return np.array(y[:N + M - 1])
```
- Trim the output to the expected linear convolution length

---

## ✅ Summary

| Step | Purpose |
|------|---------|
| Pad filter & signal | Prepare for FFT |
| Choose block size | Balance speed & memory |
| FFT & IFFT | Perform convolution efficiently |
| Overlap M-1 samples | Maintain continuity |
| Discard first M-1 samples | Eliminate circular convolution artifacts |

---

## 🧠 Notes
- This is the **canonical Overlap-Save algorithm**.
- It is especially useful when:
  - The signal is very long
  - You want **real-time or streaming** convolution
- Alternative: [Overlap-Add Method](https://en.wikipedia.org/wiki/Overlap%E2%80%93add_method), which pads the signal instead of overlapping.
