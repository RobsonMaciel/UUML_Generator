// SaveData.h
#pragma once

#include "CoreMinimal.h"
#include "SaveData.generated.h"

UCLASS()
class YOURPROJECT_API ASaveData {
    GENERATED_BODY()

public:
    ASaveData();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Save")
    int PlayerLevel;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Save")
    int PlayerExperience;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Save")
    TArray<class AItem*> InventoryItems;

    UFUNCTION(BlueprintCallable, Category = "Save")
    void Save();

    UFUNCTION(BlueprintCallable, Category = "Save")
    void Load();
}
