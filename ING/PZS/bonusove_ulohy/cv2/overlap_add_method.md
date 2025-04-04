
# 📚 Overlap-Add Method for Fast Convolution

The **Overlap-Add Method** is another fast convolution technique based on the **Fast Fourier Transform (FFT)**. It's used to efficiently compute the **linear convolution** of long signals, similar to the Overlap-Save method.

---

## 🔧 Overview

Given:
- Input signal: \( x[n] \) of length \( N \)
- Impulse response (filter): \( h[n] \) of length \( M \)
- Block size: \( L \), typically \( L = B - M + 1 \)

---

## ⚙️ Key Steps

### 1. **Choose Block Size**
- Select an FFT size \( B \) (typically a power of 2) such that \( B \geq M \)
- Define block length \( L = B - M + 1 \)

---

### 2. **Preprocessing**
```python
h_fft = np.fft.fft(h, B)
```
- Zero-pad the impulse response `h` to length `B`
- Precompute its FFT

---

### 3. **Divide Signal Into Non-Overlapping Blocks**
```python
for i in range(0, len(x), L):
    x_block = x[i:i + L]
    x_block_padded = np.concatenate([x_block, np.zeros(B - L)])
```
- Split input into **non-overlapping** blocks of length `L`
- Each block is **zero-padded** to length `B`

---

### 4. **FFT Convolution**
```python
X = np.fft.fft(x_block_padded)
Y = np.fft.ifft(X * h_fft).real
```
- Multiply in the frequency domain
- IFFT to get time-domain result

---

### 5. **Add Overlapping Segments**
```python
y[start:start + B] += Y
```
- Add the result into the output array
- Overlapping sections are summed

---

### 6. **Return Final Output**
```python
return y[:N + M - 1]
```
- Trim to the expected output length

---

## ✅ Summary

| Step | Purpose |
|------|---------|
| Divide into blocks | Efficient processing |
| Zero-pad to FFT size | Prevent circular aliasing |
| FFT & IFFT | Fast convolution |
| Add overlapping segments | Assemble final result |

---

## 🔄 Comparison: Overlap-Add vs. Overlap-Save

| Feature               | Overlap-Add                  | Overlap-Save                 |
|----------------------|------------------------------|------------------------------|
| Input blocks         | Non-overlapping              | Overlapping (M - 1 samples)  |
| Padding              | At end of each block         | At start of entire signal    |
| Output handling      | Add overlapping FFT results  | Discard start of each FFT    |
| Used when            | Real-time block convolution  | Continuous stream processing |
| Memory usage         | Slightly higher              | Slightly lower               |

---

## 🧠 Notes
- Both methods are widely used.
- Overlap-Add is generally **easier** to implement when output must be assembled from independent blocks.
- Overlap-Save is more natural for **streaming data** and continuous signals.
