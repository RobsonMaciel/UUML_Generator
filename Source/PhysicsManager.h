// PhysicsManager.h
#pragma once

#include "CoreMinimal.h"
#include "PhysicsManager.generated.h"

UCLASS()
class YOURPROJECT_API APhysicsManager {
    GENERATED_BODY()

public:
    APhysicsManager();

    UFUNCTION(BlueprintCallable, Category = "Physics")
    void ApplyGravity();

    UFUNCTION(BlueprintCallable, Category = "Physics")
    void DetectCollisions();

    UFUNCTION(BlueprintCallable, Category = "Physics")
    void ResolveCollision(class AGameObject* obj1, class AGameObject* obj2);
}
