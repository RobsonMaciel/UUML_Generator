// Weapon.h
#pragma once

#include "CoreMinimal.h"
#include "Weapon.generated.h"

UCLASS()
class YOURPROJECT_API AWeapon {
    GENERATED_BODY()

public:
    AWeapon();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    FString Name;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    int Damage;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    float Range;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Attributes")
    float Weight;

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Equip();

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Unequip();

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Reload();

    UFUNCTION(BlueprintCallable, Category = "Actions")
    void Upgrade();
}
