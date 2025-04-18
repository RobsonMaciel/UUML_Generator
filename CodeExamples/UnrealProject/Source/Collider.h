// Collider.h
#pragma once

#include "CoreMinimal.h"
#include "Collider.generated.h"

UCLASS()
class YOURPROJECT_API ACollider {
    GENERATED_BODY()

public:
    ACollider();

    UFUNCTION(BlueprintCallable, Category = "Collision")
    void DetectCollision(class AGameObject* other);

    UFUNCTION(BlueprintCallable, Category = "Collision")
    void SetTrigger(bool isTrigger);
}
