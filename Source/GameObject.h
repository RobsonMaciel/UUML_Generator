// GameObject.h
#pragma once

#include "CoreMinimal.h"
#include "GameObject.generated.h"

UCLASS()
class YOURPROJECT_API AGameObject {
    GENERATED_BODY()

public:
    AGameObject();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Object")
    FString Name;

    UFUNCTION(BlueprintCallable, Category = "Object")
    void Destroy();

    UFUNCTION(BlueprintCallable, Category = "Object")
    void SetActive(bool isActive);
}
