// Scene.h
#pragma once

#include "CoreMinimal.h"
#include "Scene.generated.h"

UCLASS()
class YOURPROJECT_API AScene {
    GENERATED_BODY()

public:
    AScene();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Scene")
    FString Name;

    UFUNCTION(BlueprintCallable, Category = "Scene")
    void LoadScene();

    UFUNCTION(BlueprintCallable, Category = "Scene")
    void UnloadScene();
}
