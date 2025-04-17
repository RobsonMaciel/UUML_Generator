// CameraController.h
#pragma once

#include "CoreMinimal.h"
#include "CameraController.generated.h"

UCLASS()
class YOURPROJECT_API ACameraController {
    GENERATED_BODY()

public:
    ACameraController();

    UFUNCTION(BlueprintCallable, Category = "Camera")
    void FollowPlayer(class ACharacter* player);

    UFUNCTION(BlueprintCallable, Category = "Camera")
    void SetCameraAngle(float angle);

    UFUNCTION(BlueprintCallable, Category = "Camera")
    void Zoom(float amount);
}
