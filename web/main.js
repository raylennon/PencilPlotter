let [BASE_SEPARATION, UPPER_LENGTH, FOREARM_LENGTH] = await eel.get_sizes()();

document.getElementById('upperL').style.position = "absolute";
document.getElementById('upperR').style.position = "absolute";

document.getElementById('upperL').style.left = window.innerWidth/2 - BASE_SEPARATION/2 + 'px';
document.getElementById('foreL').style.left = window.innerWidth/2 - BASE_SEPARATION/2 + 'px';
document.getElementById('upperR').style.left = window.innerWidth/2 + BASE_SEPARATION/2 + 'px';
document.getElementById('foreR').style.left = window.innerWidth/2 + BASE_SEPARATION/2 + 'px';

document.getElementById('path').style.left = window.innerWidth/2 - 30 +'px';
document.getElementById('path').style.bottom = 300 - 200 - 30 + 'px';

document.getElementById('upperL').style.width = UPPER_LENGTH + 'px';
document.getElementById('upperR').style.width = UPPER_LENGTH + 'px';
document.getElementById('foreL').style.width = FOREARM_LENGTH + 'px';
document.getElementById('foreR').style.width = FOREARM_LENGTH + 'px';


async function updateRotations() {
    // Get the rotation angle from Python
    let [a1, a2, a3, a4, px, py] = await eel.get_rotation_angle()();
    // Apply the rotation to the rectangle
    document.getElementById('pointer').style.left = window.innerWidth/2 + px+"px";
    document.getElementById('pointer').style.bottom = 300-py+"px";

    document.getElementById('upperL').style.transform = `rotate(${a1 * 180/Math.PI}deg)`;
    document.getElementById('upperR').style.transform = `rotate(${a2 * 180/Math.PI}deg)`;

    document.getElementById('foreL').style.transform = `translateX(${UPPER_LENGTH * Math.cos(a1)}px) translateY(${UPPER_LENGTH * Math.sin(a1)}px) rotate(${a3 * 180/Math.PI}deg)`;
    document.getElementById('foreR').style.transform = `translateX(${UPPER_LENGTH * Math.cos(a2)}px) translateY(${UPPER_LENGTH * Math.sin(a2)}px) rotate(${a4 * 180/Math.PI}deg)`;
    // Call the function again after a short delay
    setTimeout(updateRotations, 10); // Approximately 60 frames per second
}

// Start the rotation
updateRotations();
