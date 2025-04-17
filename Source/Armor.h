// Armor.h
#pragma once

#include "CoreMinimal.h"
#include "Armor.generated.h"

UCLASS()
class YOURPROJECT_API AArmor {
    GENERATED_BODY()

public:
    AArmor();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    FString Name;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    int Defense;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    float Weight;

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Equip();

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Unequip();

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Upgrade();
}
