// Inventory.h
#pragma once

#include "CoreMinimal.h"
#include "Inventory.generated.h"

UCLASS()
class YOURPROJECT_API AInventory {
    GENERATED_BODY()

public:
    AInventory();

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Items")
    TArray<class AWeapon*> Weapons;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Items")
    TArray<class AArmor*> Armors;

    UPROPERTY(EditAnywhere, BlueprintReadWrite, Category = "Items")
    TArray<class AItem*> Items;

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void AddItem(AItem* item);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void RemoveItem(AItem* item);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void UseItem(AItem* item);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void EquipWeapon(AWeapon* weapon);

    UFUNCTION(BlueprintCallable, Category = "Inventory")
    void EquipArmor(AArmor* armor);
}
