# Python3 code to demonstrate to draw
# circle without floating
# point arithmetic

def drawCircle(r):
    # Consider a rectangle of size N*N
    N = 2 * r + 1

    # Draw a square of size N*N.
    for i in range(N):
        for j in range(N):

            # Start from the left most corner point
            x = i - r
            y = j - r

            # If this point is inside the circle,
            # print it
            if x * x + y * y <= r * r + 1:
                print(".", end=" ")

                # If outside the circle, print space
            else:
                print(" ", end=" ")
        print()

    # Driver Code


if __name__ == "__main__":
    drawCircle(1)

# This code is contributed
# by vibhu4agarwal
