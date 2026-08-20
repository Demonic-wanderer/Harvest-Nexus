# ==========================================
# KISAN AI - TEST PROGRAM
# ==========================================

print("Starting Kisan AI test...")
print()


# ==========================================
# TEST 1: PYTORCH
# ==========================================

try:
    import torch

    print("✅ PyTorch is working")
    print("   Version:", torch.__version__)

except Exception as e:

    print("❌ PyTorch problem")
    print("   Error:", e)


print()


# ==========================================
# TEST 2: PILLOW
# ==========================================

try:
    from PIL import Image

    print("✅ Pillow is working")

except Exception as e:

    print("❌ Pillow problem")
    print("   Error:", e)


print()


# ==========================================
# TEST 3: TRANSFORMERS
# ==========================================

try:
    import transformers

    print("✅ Transformers is working")
    print("   Version:", transformers.__version__)

except Exception as e:

    print("❌ Transformers problem")
    print("   Error:", e)


print()


# ==========================================
# TEST 4: ACCELERATE
# ==========================================

try:
    import accelerate

    print("✅ Accelerate is working")
    print("   Version:", accelerate.__version__)

except Exception as e:

    print("❌ Accelerate problem")
    print("   Error:", e)


print()


# ==========================================
# TEST 5: CHECK GPU
# ==========================================

try:

    import torch

    if torch.cuda.is_available():

        print("✅ NVIDIA GPU detected")
        print("   GPU:", torch.cuda.get_device_name(0))

    else:

        print("ℹ️ No NVIDIA GPU detected")
        print("   AI can still run on CPU.")

except Exception as e:

    print("❌ GPU test problem")
    print("   Error:", e)


print()


# ==========================================
# FINAL RESULT
# ==========================================

print("==========================================")
print("          KISAN AI TEST FINISHED")
print("==========================================")

print()
print("If you see ✅ for PyTorch,")
print("Pillow, Transformers and Accelerate,")
print("your Python environment is ready.")