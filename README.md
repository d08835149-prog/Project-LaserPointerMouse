# LaserPointerMouse

LaserPointerMouse is a project that uses a **Raspberry Pi Zero 2 W** and a **Raspberry Pi Camera Module 3** to track a laser pointer and use its position as mouse input.

The camera detects the laser point, and the Raspberry Pi processes the camera image to determine its position.

## Why I Made This

I wanted to make a project where I could control a computer using a laser pointer instead of a normal mouse.

I also wanted to learn more about Raspberry Pi, computer vision, camera processing, and designing a custom case for hardware.

## How It Works

The Raspberry Pi Camera Module 3 captures video of the area where the laser pointer is being used.

The Raspberry Pi Zero 2 W processes the camera image and detects the bright laser point.

The detected position is converted into coordinates that can be used to control the mouse cursor.

Basic process:

**Laser Pointer → Camera → Raspberry Pi Zero 2 W → Image Processing → Mouse Movement**

## Hardware

* Raspberry Pi Zero 2 W
* Raspberry Pi Camera Module 3
* Raspberry Pi camera cable
* 5V power supply
* Custom 3D printed case

## Hardware Connections

The hardware connection is simple because the camera connects directly to the Raspberry Pi.

**Camera Module 3 → Camera Cable → Raspberry Pi Zero 2 W Camera Connector**

The Raspberry Pi Zero 2 W receives power through its USB power port.

No external breadboard circuit is required for the main system.

## CAD

I designed the enclosure for LaserPointerMouse using **Tinkercad**.

The case is designed to hold and protect the Raspberry Pi Zero 2 W and camera while keeping the camera positioned correctly.

The CAD files are included in this repository.

## Software

The software runs on the Raspberry Pi Zero 2 W.

It receives images from the Camera Module 3, detects the laser point, calculates its position, and converts that position into mouse movement.

## Wiring Diagram

The wiring diagram shows the connection between:

**Raspberry Pi Camera Module 3 → Camera Cable → Raspberry Pi Zero 2 W → 5V Power**

## What I Learned

Through this project, I learned more about:

* Raspberry Pi hardware
* Raspberry Pi camera connections
* Computer vision and image processing
* Connecting software with physical hardware
* Designing a case in Tinkercad
* 3D printing and CAD

## Future Improvements

Some possible improvements are:

* Improve laser detection accuracy
* Reduce cursor movement delay
* Improve calibration
* Make the enclosure smaller and cleaner
* Improve camera mounting
* Add more mouse controls and gestures

## Project Files

The repository includes the source code, CAD files, wiring diagram, and other files needed to understand and reproduce the project.
